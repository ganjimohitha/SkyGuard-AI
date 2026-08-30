import pandas as pd
import numpy as np


# ============================================================
# PATHS
# ============================================================

INPUT_PATH = "data/processed/aws_anomaly_dataset.csv"
OUTPUT_PATH = "data/processed/aws_temporal_evaluation.csv"


# ============================================================
# CONFIGURATION
# ============================================================

# Dataset is 3-hourly, so:
#
# 8 observations  = 24 hours
# 16 observations = 48 hours
# 24 observations = 72 hours

FROZEN_WINDOW = 8
DRIFT_WINDOW = 8

# A sensor reporting exactly/nearly the same value
# repeatedly for 24 hours is suspicious.
FROZEN_STD_THRESHOLD = 0.05

# Persistent movement over the window.
DRIFT_CHANGE_THRESHOLD = 3.0


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print("Loading SkyGuard anomaly dataset...")

    df = pd.read_csv(
        INPUT_PATH,
        parse_dates=["timestamp"]
    )

    df = df.sort_values(
        ["station_id", "timestamp"]
    ).reset_index(drop=True)

    print(f"Rows: {len(df):,}")
    print(f"Stations: {df['station_id'].nunique()}")

    return df


# ============================================================
# FROZEN SENSOR DETECTION
# ============================================================

def detect_frozen_sensor(df):

    print("\nDetecting frozen sensor patterns...")

    # Rolling standard deviation within each station.
    #
    # A very low standard deviation over several consecutive
    # observations means the sensor has barely changed.

    rolling_std = (
        df.groupby("station_id")["temperature"]
        .transform(
            lambda x: x.rolling(
                window=FROZEN_WINDOW,
                min_periods=FROZEN_WINDOW
            ).std()
        )
    )

    frozen_flag = (
        rolling_std <= FROZEN_STD_THRESHOLD
    )

    # Require the current temperature to be identical/nearly
    # identical to the previous value as additional evidence.

    previous_temperature = (
        df.groupby("station_id")["temperature"]
        .shift(1)
    )

    consecutive_difference = (
        (df["temperature"] - previous_temperature)
        .abs()
    )

    frozen_flag = (
        frozen_flag
        & (consecutive_difference <= FROZEN_STD_THRESHOLD)
    )

    return frozen_flag.fillna(False)


# ============================================================
# TEMPERATURE DRIFT DETECTION
# ============================================================
def detect_temperature_drift(df):

    print("Detecting temperature drift patterns...")

    temperature_difference = (
        df.groupby("station_id")["temperature"]
        .diff()
    )

    # Count consecutive positive and negative movements.
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

    # Total temperature movement.
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

    # Net movement over the complete window.
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

    # Require strong directional consistency AND
    # substantial movement.
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
# EVALUATE AGAINST GROUND TRUTH
# ============================================================

def evaluate_detector(
    df,
    prediction_column,
    anomaly_type
):

    actual = (
        df["anomaly_type"] == anomaly_type
    )

    predicted = df[prediction_column]

    true_positive = (
        actual & predicted
    ).sum()

    false_positive = (
        (~actual) & predicted
    ).sum()

    false_negative = (
        actual & (~predicted)
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

    print(f"\n{anomaly_type}")

    print(f"  Actual anomalies: {actual.sum():,}")
    print(f"  Detected:         {true_positive:,}")
    print(f"  False positives:  {false_positive:,}")
    print(f"  Precision:        {precision:.4f}")
    print(f"  Recall:           {recall:.4f}")
    print(f"  F1:               {f1:.4f}")

    return {
        "anomaly_type": anomaly_type,
        "actual": int(actual.sum()),
        "detected": int(true_positive),
        "false_positives": int(false_positive),
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("========================================")
    print("SkyGuard Temporal Anomaly Detector")
    print("========================================")

    df = load_data()

    # --------------------------------------------------------
    # Frozen sensor
    # --------------------------------------------------------

    df["temporal_frozen"] = detect_frozen_sensor(df)

    # --------------------------------------------------------
    # Temperature drift
    # --------------------------------------------------------

    df["temporal_drift"] = detect_temperature_drift(df)

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print("\n========== TEMPORAL DETECTOR RESULTS ==========")

    results = []

    results.append(
        evaluate_detector(
            df,
            "temporal_frozen",
            "frozen_sensor"
        )
    )

    results.append(
        evaluate_detector(
            df,
            "temporal_drift",
            "temperature_drift"
        )
    )

    results_df = pd.DataFrame(results)

    print("\n========== SUMMARY ==========")

    print(
        results_df.to_string(
            index=False,
            formatters={
                "precision": "{:.4f}".format,
                "recall": "{:.4f}".format,
                "f1": "{:.4f}".format,
            }
        )
    )

    # --------------------------------------------------------
    # Save evaluation data
    # --------------------------------------------------------

    df[
        [
            "timestamp",
            "station_id",
            "temperature",
            "pressure",
            "humidity",
            "anomaly_type",
            "is_anomaly",
            "temporal_frozen",
            "temporal_drift",
        ]
    ].to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\nSaved temporal evaluation data to:")
    print(OUTPUT_PATH)

    print("\n========================================")
    print("Temporal detection complete.")
    print("========================================")


if __name__ == "__main__":
    main()