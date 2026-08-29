from pathlib import Path
from zipfile import ZipFile
import pandas as pd


ZIP_PATH = Path("data/raw/antaws/The AntAWS dataset/3_hourly.zip")


def main():
    print("Profiling AntAWS station date coverage...\n")

    results = []

    with ZipFile(ZIP_PATH, "r") as z:

        csv_files = [
            name
            for name in z.namelist()
            if name.startswith("3_hourly/")
            and name.lower().endswith(".csv")
        ]

        for index, csv_path in enumerate(csv_files, start=1):

            station_id = Path(csv_path).stem.replace("_3h", "")

            try:
                df = pd.read_csv(
                    z.open(csv_path),
                    encoding="latin1"
                )
            except Exception as e:
                print(f"Skipping {station_id}: {e}")
                continue

            required = [
                "Temperature(¡æ)",
                "Pressure(hPa)",
                "Relative Humidity(%)",
            ]

            if not all(col in df.columns for col in required):
                continue

            complete = df.dropna(subset=required).copy()

            if complete.empty:
                continue

            complete["timestamp"] = pd.to_datetime(
                complete["Year"].astype(str)
                + "-"
                + complete["Month"].astype(str)
                + "-"
                + complete["Day"].astype(str)
                + " "
                + complete["Three-hourly observation time(UTC)"].astype(str)
                + ":00",
                errors="coerce"
            )

            complete = complete.dropna(subset=["timestamp"])

            if complete.empty:
                continue

            results.append({
                "station_id": station_id,
                "complete_tprh": len(complete),
                "start_date": complete["timestamp"].min(),
                "end_date": complete["timestamp"].max(),
                "years_covered": round(
                    (
                        complete["timestamp"].max()
                        - complete["timestamp"].min()
                    ).days / 365.25,
                    2
                ),
            })

            if index % 25 == 0:
                print(f"Processed {index}/{len(csv_files)} stations...")

    summary = pd.DataFrame(results)

    summary = summary.sort_values(
        ["complete_tprh", "years_covered"],
        ascending=[False, False]
    )

    print("\n========== DATE COVERAGE ==========\n")

    print(
        summary.head(30).to_string(index=False)
    )

    output = Path("data/antaws_station_profile.csv")
    summary.to_csv(output, index=False)

    print("\n===================================\n")
    print(f"Stations profiled: {len(summary)}")
    print(f"Saved to: {output}")


if __name__ == "__main__":
    main()