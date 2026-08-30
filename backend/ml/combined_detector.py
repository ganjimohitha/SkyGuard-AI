from pathlib import Path
from xml.parsers.expat import model

import joblib
import numpy as np
import pandas as pd


# ============================================================
# PATHS
# ============================================================

DATA_PATH = Path("data/processed/aws_anomaly_dataset.csv")
MODEL_PATH = Path("models/isolation_forest.joblib")
OUTPUT_PATH = Path("data/processed/aws_combined_predictions.csv")


# ============================================================
# CONFIGURATION
# ============================================================

DRIFT_WINDOW = 8

FROZEN_WINDOW = 8
FROZEN_STD_THRESHOLD = 0.05

DRIFT_CHANGE_THRESHOLD = 3.0


# ============================================================
# FEATURES
# ============================================================

FEATURES = [
    "temperature",
    "pressure",
    "humidity",
    "hour",
    "month",
    "day_of_year",
    "month_sin",
    "month_cos",
    "hour_sin",
    "hour_cos",
    "temperature_diff",
    "temperature_diff_abs",
    "pressure_diff",
    "pressure_diff_abs",
    "humidity_diff",
    "humidity_diff_abs",
    "temperature_rolling_mean",
    "temperature_rolling_std",
    "temperature_deviation",
    "pressure_rolling_mean",
    "pressure_rolling_std",
    "pressure_deviation",
    "humidity_rolling_mean",
    "humidity_rolling_std",
    "humidity_deviation",
    "temperature_humidity_interaction",
    "original_temperature",
    "original_pressure",
    "original_humidity",
]


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print("Loading SkyGuard anomaly dataset...")

    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["timestamp"]
    )

    df = df.sort_values(
        ["station_id", "timestamp"]
    ).reset_index(drop=True)

    print(f"Rows: {len(df):,}")
    print(f"Stations: {df['station_id'].nunique()}")

    return df


# ============================================================
# ISOLATION FOREST
# ============================================================

# def run_isolation_forest(df):

#     print("\nRunning Isolation Forest...")

#     saved = joblib.load(MODEL_PATH)

#     model = saved["model"]

#     model_features = saved["features"]

#     X = df[FEATURES]

#     predictions = model.predict(X)  

#     # Isolation Forest:
#     #  1  = normal
#     # -1  = anomaly

#     anomaly_flag = predictions == -1

#     # Larger positive score means more anomalous.
#     anomaly_score = -model.decision_function(X)

#     print(
#         f"Isolation Forest anomalies: "
#         f"{anomaly_flag.sum():,}"
#     )

    # return anomaly_flag, anomaly_score

def run_isolation_forest(df):

    print("\nRunning Isolation Forest...")

    saved = joblib.load(MODEL_PATH)

    model = saved["model"]
    model_features = saved["features"]

    print(
        f"Features expected by model: "
        f"{len(model_features)}"
    )

    missing_features = [
        feature
        for feature in model_features
        if feature not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing model features: {missing_features}"
        )

    X = df[model_features]

    predictions = model.predict(X)

    # Isolation Forest:
    #  1  = normal
    # -1  = anomaly

    anomaly_flag = predictions == -1

    # Larger positive value = more anomalous.
    anomaly_score = -model.decision_function(X)

    print(
        f"Isolation Forest anomalies: "
        f"{anomaly_flag.sum():,}"
    )

    return anomaly_flag, anomaly_score


# ============================================================
# FROZEN SENSOR
# ============================================================

def detect_frozen_sensor(df):

    print("Running frozen sensor detector...")

    rolling_std = (
        df.groupby("station_id")["temperature"]
        .transform(
            lambda x: x.rolling(
                window=FROZEN_WINDOW,
                min_periods=FROZEN_WINDOW
            ).std()
        )
    )

    previous_temperature = (
        df.groupby("station_id")["temperature"]
        .shift(1)
    )

    consecutive_difference = (
        (
            df["temperature"]
            - previous_temperature
        )
        .abs()
    )

    frozen_flag = (
        (rolling_std <= FROZEN_STD_THRESHOLD)
        & (
            consecutive_difference
            <= FROZEN_STD_THRESHOLD
        )
    )

    return frozen_flag.fillna(False)


# ============================================================
# TEMPERATURE DRIFT
# ============================================================

def detect_temperature_drift(df):

    print("Running temperature drift detector...")

    temperature_difference = (
        df.groupby("station_id")["temperature"]
        .diff()
    )

    positive_changes = (
        (temperature_difference > 0.5)
        .astype(int)
        .groupby(df["station_id"])
        .transform(
            lambda x: x.rolling(
                window=DRIFT_WINDOW - 1,
                min_periods=DRIFT_WINDOW - 1
            ).sum()
        )
    )

    negative_changes = (
        (temperature_difference < -0.5)
        .astype(int)
        .groupby(df["station_id"])
        .transform(
            lambda x: x.rolling(
                window=DRIFT_WINDOW - 1,
                min_periods=DRIFT_WINDOW - 1
            ).sum()
        )
    )

    absolute_change = (
        temperature_difference.abs()
        .groupby(df["station_id"])
        .transform(
            lambda x: x.rolling(
                window=DRIFT_WINDOW - 1,
                min_periods=DRIFT_WINDOW - 1
            ).sum()
        )
    )

    net_change = (
        temperature_difference
        .groupby(df["station_id"])
        .transform(
            lambda x: x.rolling(
                window=DRIFT_WINDOW - 1,
                min_periods=DRIFT_WINDOW - 1
            ).sum()
        )
    )

    positive_drift = (
        (positive_changes >= 6)
        & (net_change >= 10.0)
        & (absolute_change >= 10.0)
    )

    negative_drift = (
        (negative_changes >= 6)
        & (net_change <= -10.0)
        & (absolute_change >= 10.0)
    )

    drift_flag = (
        positive_drift
        | negative_drift
    )

    return drift_flag.fillna(False)


# ============================================================
# COMBINE DETECTORS
# ============================================================

def combine_predictions(
    isolation_flag,
    frozen_flag,
    drift_flag,
    isolation_score
):

    combined_flag = (
        isolation_flag
        | frozen_flag
        | drift_flag
    )

    anomaly_type = np.where(
        frozen_flag,
        "frozen_sensor",
        np.where(
            drift_flag,
            "temperature_drift",
            np.where(
                isolation_flag,
                "statistical_anomaly",
                "normal"
            )
        )
    )

    return combined_flag, anomaly_type


# ============================================================
# MAIN
# ============================================================

def main():

    print("========================================")
    print("SkyGuard Combined Anomaly Detector")
    print("========================================")

    df = load_data()

    # --------------------------------------------------------
    # Isolation Forest
    # --------------------------------------------------------

    isolation_flag, isolation_score = (
        run_isolation_forest(df)
    )

    # --------------------------------------------------------
    # Temporal detectors
    # --------------------------------------------------------

    frozen_flag = detect_frozen_sensor(df)

    drift_flag = detect_temperature_drift(df)

    # --------------------------------------------------------
    # Combine
    # --------------------------------------------------------

    combined_flag, anomaly_type = (
        combine_predictions(
            isolation_flag,
            frozen_flag,
            drift_flag,
            isolation_score
        )
    )

    # --------------------------------------------------------
    # Store predictions
    # --------------------------------------------------------

    df["isolation_anomaly"] = (
        isolation_flag.astype(int)
    )

    df["isolation_score"] = (
        isolation_score
    )

    df["temporal_frozen"] = (
        frozen_flag.astype(int)
    )

    df["temporal_drift"] = (
        drift_flag.astype(int)
    )

    df["combined_anomaly"] = (
        combined_flag.astype(int)
    )

    df["predicted_anomaly_type"] = (
        anomaly_type
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print("\n========== COMBINED RESULTS ==========")

    print(
        f"Isolation Forest anomalies: "
        f"{isolation_flag.sum():,}"
    )

    print(
        f"Frozen sensor anomalies:    "
        f"{frozen_flag.sum():,}"
    )

    print(
        f"Temperature drift:          "
        f"{drift_flag.sum():,}"
    )

    print(
        f"Combined anomalies:         "
        f"{combined_flag.sum():,}"
    )

    print(
        f"Combined anomaly rate:      "
        f"{combined_flag.mean() * 100:.2f}%"
    )

    print("\nPredicted anomaly types:")

    print(
        pd.Series(anomaly_type)
        .value_counts()
        .to_string()
    )

    # --------------------------------------------------------
    # Ground-truth comparison
    # --------------------------------------------------------

    if "is_anomaly" in df.columns:

        actual = (
            df["is_anomaly"] == 1
        )

        true_positive = (
            actual & combined_flag
        ).sum()

        false_positive = (
            (~actual) & combined_flag
        ).sum()

        false_negative = (
            actual & (~combined_flag)
        ).sum()

        precision = (
            true_positive
            / (true_positive + false_positive)
            if (true_positive + false_positive) > 0
            else 0
        )

        recall = (
            true_positive
            / (true_positive + false_negative)
            if (true_positive + false_negative) > 0
            else 0
        )

        f1 = (
            2 * precision * recall
            / (precision + recall)
            if (precision + recall) > 0
            else 0
        )

        print("\n========== OVERALL PERFORMANCE ==========")

        print(
            f"True positives:  {true_positive:,}"
        )

        print(
            f"False positives: {false_positive:,}"
        )

        print(
            f"False negatives: {false_negative:,}"
        )

        print(
            f"Precision:       {precision:.4f}"
        )

        print(
            f"Recall:          {recall:.4f}"
        )

        print(
            f"F1 Score:        {f1:.4f}"
        )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df[
        [
            "timestamp",
            "station_id",
            "temperature",
            "pressure",
            "humidity",
            "is_anomaly",
            "anomaly_type",
            "isolation_anomaly",
            "isolation_score",
            "temporal_frozen",
            "temporal_drift",
            "combined_anomaly",
            "predicted_anomaly_type",
        ]
    ].to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\nSaved to:")
    print(OUTPUT_PATH)

    print("\n========================================")
    print("Combined detection complete.")
    print("========================================")


if __name__ == "__main__":
    main()