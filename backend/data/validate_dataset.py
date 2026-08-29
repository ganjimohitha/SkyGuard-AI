from pathlib import Path

import pandas as pd


DATA_PATH = Path(
    "data/processed/aws_training_data.csv"
)


def main():

    print("Validating SkyGuard dataset...\n")

    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["timestamp"]
    )

    print("========== BASIC INFO ==========")

    print(f"Rows: {len(df):,}")
    print(f"Stations: {df['station_id'].nunique()}")
    print(f"Columns: {df.columns.tolist()}")

    print("\n========== MISSING VALUES ==========")
    print(df.isna().sum())

    print("\n========== DUPLICATES ==========")

    duplicates = df.duplicated(
        subset=["station_id", "timestamp"]
    ).sum()

    print(
        f"Duplicate station/timestamp rows: {duplicates:,}"
    )

    print("\n========== SENSOR RANGES ==========")

    for column in [
        "temperature",
        "pressure",
        "humidity",
    ]:
        print(f"\n{column}")
        print(f"  Min: {df[column].min()}")
        print(f"  Max: {df[column].max()}")
        print(f"  Mean: {df[column].mean():.2f}")
        print(f"  Std: {df[column].std():.2f}")

    print("\n========== SUSPICIOUS VALUES ==========")

    checks = {
        "temperature < -90": df["temperature"] < -90,
        "temperature > 60": df["temperature"] > 60,
        "pressure < 800": df["pressure"] < 800,
        "pressure > 1100": df["pressure"] > 1100,
        "humidity < 0": df["humidity"] < 0,
        "humidity > 100": df["humidity"] > 100,
    }

    for name, condition in checks.items():
        print(
            f"{name}: {condition.sum():,}"
        )

    print("\n========== STATION COUNTS ==========")

    station_counts = (
        df.groupby("station_id")
        .size()
        .sort_values(ascending=False)
    )

    print(station_counts.to_string())

    print("\n========== TIME RANGE PER STATION ==========")

    station_dates = (
        df.groupby("station_id")["timestamp"]
        .agg(["min", "max", "count"])
        .sort_values("count", ascending=False)
    )

    print(
        station_dates.to_string()
    )

    print("\n====================================")
    print("Dataset validation complete.")
    print("====================================")


if __name__ == "__main__":
    main()