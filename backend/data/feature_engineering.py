from pathlib import Path

import numpy as np
import pandas as pd


INPUT_PATH = Path(
    "data/processed/aws_training_data.csv"
)

OUTPUT_PATH = Path(
    "data/processed/aws_features.csv"
)


def add_features(df):

    df = df.sort_values(
        ["station_id", "timestamp"]
    ).copy()

    # --------------------------------------------------
    # Time features
    # --------------------------------------------------

    df["hour"] = df["timestamp"].dt.hour

    df["month"] = df["timestamp"].dt.month

    df["day_of_year"] = (
        df["timestamp"].dt.dayofyear
    )

    # Cyclic encoding prevents December (12)
    # from appearing far away from January (1).

    df["month_sin"] = np.sin(
        2 * np.pi * df["month"] / 12
    )

    df["month_cos"] = np.cos(
        2 * np.pi * df["month"] / 12
    )

    df["hour_sin"] = np.sin(
        2 * np.pi * df["hour"] / 24
    )

    df["hour_cos"] = np.cos(
        2 * np.pi * df["hour"] / 24
    )

    # --------------------------------------------------
    # Temporal change features
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Rolling statistics
    # --------------------------------------------------

    for column in [
        "temperature",
        "pressure",
        "humidity",
    ]:

        grouped = df.groupby(
            "station_id"
        )[column]

        df[f"{column}_rolling_mean"] = (
            grouped
            .transform(
                lambda x: x.rolling(
                    window=5,
                    min_periods=2
                ).mean()
            )
        )

        df[f"{column}_rolling_std"] = (
            grouped
            .transform(
                lambda x: x.rolling(
                    window=5,
                    min_periods=2
                ).std()
            )
        )

        # Distance from recent local behavior
        df[f"{column}_deviation"] = (
            df[column]
            - df[f"{column}_rolling_mean"]
        )

    # --------------------------------------------------
    # Physical consistency features
    # --------------------------------------------------

    # Temperature-humidity relationship indicator.
    # We don't classify it as anomalous here.
    df["temperature_humidity_interaction"] = (
        df["temperature"]
        * df["humidity"]
    )

    # --------------------------------------------------
    # Remove rows where rolling/difference features
    # cannot yet be calculated.
    # --------------------------------------------------

    feature_columns = [
        "temperature_diff",
        "pressure_diff",
        "humidity_diff",
        "temperature_rolling_std",
        "pressure_rolling_std",
        "humidity_rolling_std",
    ]

    df = df.dropna(
        subset=feature_columns
    ).reset_index(drop=True)

    return df


def main():

    print("Creating SkyGuard ML features...\n")

    df = pd.read_csv(
        INPUT_PATH,
        parse_dates=["timestamp"]
    )

    print(
        f"Input rows: {len(df):,}"
    )

    feature_df = add_features(df)

    print(
        f"Output rows: {len(feature_df):,}"
    )

    print(
        f"Features created: "
        f"{len(feature_df.columns)}"
    )

    print("\nColumns:")

    for column in feature_df.columns:
        print(f"  - {column}")

    print("\nMissing values:")

    print(
        feature_df.isna().sum()
    )

    feature_df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\nSaved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()