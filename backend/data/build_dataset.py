from pathlib import Path
from zipfile import ZipFile

import pandas as pd


ZIP_PATH = Path(
    "data/raw/antaws/The AntAWS dataset/3_hourly.zip"
)

SUMMARY_PATH = Path(
    "data/antaws_station_profile.csv"
)

OUTPUT_DIR = Path("data/processed")
OUTPUT_PATH = OUTPUT_DIR / "aws_training_data.csv"


TOP_N_STATIONS = 15


def build_timestamp(df):
    return pd.to_datetime(
        df["Year"].astype(str)
        + "-"
        + df["Month"].astype(str).str.zfill(2)
        + "-"
        + df["Day"].astype(str).str.zfill(2)
        + " "
        + df["Three-hourly observation time(UTC)"]
        .astype(str)
        .str.zfill(2)
        + ":00:00",
        errors="coerce",
        utc=True,
    )


def main():

    print("Building SkyGuard training dataset...\n")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    profile = pd.read_csv(SUMMARY_PATH)

    # Select stations with the highest number
    # of complete T+P+RH observations.
    selected = (
        profile
        .sort_values(
            "complete_tprh",
            ascending=False
        )
        .head(TOP_N_STATIONS)
    )

    station_ids = selected["station_id"].tolist()

    print("Selected stations:")
    for station in station_ids:
        print(f"  - {station}")

    print()

    datasets = []

    with ZipFile(ZIP_PATH, "r") as z:

        files = z.namelist()

        for station_id in station_ids:

            filename = f"3_hourly/{station_id}_3h.csv"

            if filename not in files:
                print(
                    f"WARNING: file not found for {station_id}"
                )
                continue

            print(f"Processing: {station_id}")

            df = pd.read_csv(
                z.open(filename),
                encoding="latin1"
            )

            required_columns = [
                "Temperature(¡æ)",
                "Pressure(hPa)",
                "Relative Humidity(%)",
            ]

            missing_columns = [
                column
                for column in required_columns
                if column not in df.columns
            ]

            if missing_columns:
                print(
                    f"  Skipping {station_id}: "
                    f"missing {missing_columns}"
                )
                continue

            result = pd.DataFrame()

            result["timestamp"] = build_timestamp(df)

            result["station_id"] = station_id

            result["temperature"] = pd.to_numeric(
                df["Temperature(¡æ)"],
                errors="coerce"
            )

            result["pressure"] = pd.to_numeric(
                df["Pressure(hPa)"],
                errors="coerce"
            )

            result["humidity"] = pd.to_numeric(
                df["Relative Humidity(%)"],
                errors="coerce"
            )

            # Remove rows where one of the three
            # required sensor values is missing.
            result = result.dropna(
                subset=[
                    "timestamp",
                    "temperature",
                    "pressure",
                    "humidity",
                ]
            )

            datasets.append(result)

            print(
                f"  Complete observations: {len(result):,}"
            )

    if not datasets:
        raise RuntimeError(
            "No usable station data was found."
        )

    final_df = pd.concat(
        datasets,
        ignore_index=True
    )

    final_df = (
        final_df
        .sort_values(
            ["station_id", "timestamp"]
        )
        .drop_duplicates(
            subset=["station_id", "timestamp"]
        )
        .reset_index(drop=True)
    )

    final_df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\n========== DATASET COMPLETE ==========")

    print(
        f"Rows: {len(final_df):,}"
    )

    print(
        f"Stations: "
        f"{final_df['station_id'].nunique()}"
    )

    print(
        f"Start: {final_df['timestamp'].min()}"
    )

    print(
        f"End: {final_df['timestamp'].max()}"
    )

    print("\nColumns:")
    print(final_df.columns.tolist())

    print("\nMissing values:")
    print(final_df.isna().sum())

    print("\nSaved to:")
    print(OUTPUT_PATH)

    print("=======================================")


if __name__ == "__main__":
    main()