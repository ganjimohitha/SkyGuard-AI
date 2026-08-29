from pathlib import Path

import numpy as np
import pandas as pd


INPUT_PATH = Path("data/processed/aws_features.csv")
OUTPUT_PATH = Path("data/processed/aws_anomaly_dataset.csv")

RANDOM_SEED = 42
ANOMALY_RATE = 0.05


def main():
    print("Starting SkyGuard anomaly injection...\n")

    np.random.seed(RANDOM_SEED)

    # Load dataset
    df = pd.read_csv(
        INPUT_PATH,
        parse_dates=["timestamp"]
    )

    print(f"Input observations: {len(df):,}")

    # Make sure rows are ordered correctly
    df = df.sort_values(
        ["station_id", "timestamp"]
    ).reset_index(drop=True)

    # Preserve original sensor measurements
    for column in ["temperature", "pressure", "humidity"]:
        df[f"original_{column}"] = df[column]

    # Ground-truth labels
    df["is_anomaly"] = 0
    df["anomaly_type"] = "normal"

    # ---------------------------------------------------------
    # Select anomaly rows
    # ---------------------------------------------------------

    number_of_anomalies = int(
        len(df) * ANOMALY_RATE
    )

    anomaly_indices = np.random.choice(
        df.index,
        size=number_of_anomalies,
        replace=False
    )

    # Divide anomalies between six types
    anomaly_types = [
        "temperature_spike",
        "pressure_spike",
        "humidity_spike",
        "frozen_sensor",
        "temperature_drift",
        "multivariate_inconsistency",
    ]

    assigned_types = np.random.choice(
        anomaly_types,
        size=number_of_anomalies,
        replace=True
    )

    # ---------------------------------------------------------
    # Fast previous-value lookup
    # ---------------------------------------------------------

    previous_temperature = (
        df.groupby("station_id")["temperature"]
        .shift(1)
    )

    # ---------------------------------------------------------
    # Temperature spikes
    # ---------------------------------------------------------

    mask = (
        df.index.isin(
            anomaly_indices[assigned_types == "temperature_spike"]
        )
    )

    df.loc[mask, "temperature"] += 60.0
    df.loc[mask, "is_anomaly"] = 1
    df.loc[mask, "anomaly_type"] = "temperature_spike"

    # ---------------------------------------------------------
    # Pressure spikes
    # ---------------------------------------------------------

    mask = (
        df.index.isin(
            anomaly_indices[assigned_types == "pressure_spike"]
        )
    )

    df.loc[mask, "pressure"] -= 250.0
    df.loc[mask, "is_anomaly"] = 1
    df.loc[mask, "anomaly_type"] = "pressure_spike"

    # ---------------------------------------------------------
    # Humidity spikes
    # ---------------------------------------------------------

    mask = (
        df.index.isin(
            anomaly_indices[assigned_types == "humidity_spike"]
        )
    )

    df.loc[mask, "humidity"] = 150.0
    df.loc[mask, "is_anomaly"] = 1
    df.loc[mask, "anomaly_type"] = "humidity_spike"

    # ---------------------------------------------------------
    # Frozen sensor
    # ---------------------------------------------------------

    mask = (
        df.index.isin(
            anomaly_indices[assigned_types == "frozen_sensor"]
        )
    )

    # Only use previous value when one exists
    valid_frozen = mask & previous_temperature.notna()

    df.loc[valid_frozen, "temperature"] = (
        previous_temperature[valid_frozen]
    )

    df.loc[valid_frozen, "is_anomaly"] = 1
    df.loc[valid_frozen, "anomaly_type"] = "frozen_sensor"

    # ---------------------------------------------------------
    # Temperature drift
    # ---------------------------------------------------------

    mask = (
        df.index.isin(
            anomaly_indices[assigned_types == "temperature_drift"]
        )
    )

    df.loc[mask, "temperature"] += 8.0
    df.loc[mask, "is_anomaly"] = 1
    df.loc[mask, "anomaly_type"] = "temperature_drift"

    # ---------------------------------------------------------
    # Multivariate inconsistency
    # ---------------------------------------------------------

    mask = (
        df.index.isin(
            anomaly_indices[
                assigned_types == "multivariate_inconsistency"
            ]
        )
    )

    df.loc[mask, "temperature"] += 35.0
    df.loc[mask, "is_anomaly"] = 1
    df.loc[mask, "anomaly_type"] = (
        "multivariate_inconsistency"
    )

    # ---------------------------------------------------------
    # Recalculate difference features
    # ---------------------------------------------------------

    for column in [
        "temperature",
        "pressure",
        "humidity",
    ]:

        df[f"{column}_diff"] = (
            df.groupby("station_id")[column]
            .diff()
        )

        df[f"{column}_diff_abs"] = (
            df[f"{column}_diff"].abs()
        )

    # First observation of every station has no previous value.
    # Fill these safely so the ML dataset contains no NaN.
    difference_columns = [
        "temperature_diff",
        "temperature_diff_abs",
        "pressure_diff",
        "pressure_diff_abs",
        "humidity_diff",
        "humidity_diff_abs",
    ]

    df[difference_columns] = (
        df[difference_columns]
        .fillna(0)
    )

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\n========== INJECTION RESULTS ==========")

    print(
        f"Total observations: {len(df):,}"
    )

    print(
        f"Anomalies injected: "
        f"{df['is_anomaly'].sum():,}"
    )

    print(
        f"Actual anomaly rate: "
        f"{df['is_anomaly'].mean() * 100:.2f}%"
    )

    print("\nAnomaly distribution:")

    print(
        df.loc[
            df["is_anomaly"] == 1,
            "anomaly_type"
        ]
        .value_counts()
        .to_string()
    )

    print("\nLabels:")

    print(
        df["is_anomaly"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("\nMissing values:")

    print(
        df.isna().sum()
        .loc[lambda x: x > 0]
        .to_string()
    )

    print("\nSaved to:")
    print(OUTPUT_PATH)

    print("========================================")


if __name__ == "__main__":
    main()