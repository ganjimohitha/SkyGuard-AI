from pathlib import Path
from zipfile import ZipFile
import pandas as pd


ZIP_PATH = Path("data/raw/antaws/The AntAWS dataset/3_hourly.zip")


def analyze_station(zip_file, csv_path):
    station_id = Path(csv_path).stem.replace("_3h", "")

    try:
        df = pd.read_csv(
            zip_file.open(csv_path),
            encoding="latin1"
        )
    except Exception as e:
        print(f"Could not read {csv_path}: {e}")
        return None

    required = [
        "Temperature(¡æ)",
        "Pressure(hPa)",
        "Relative Humidity(%)",
    ]

    if not all(column in df.columns for column in required):
        return None

    complete = df.dropna(subset=required)

    return {
        "station_id": station_id,
        "total_rows": len(df),
        "temperature_available": df["Temperature(¡æ)"].notna().sum(),
        "pressure_available": df["Pressure(hPa)"].notna().sum(),
        "humidity_available": df["Relative Humidity(%)"].notna().sum(),
        "complete_tprh": len(complete),
        "complete_percentage": round(
            len(complete) / len(df) * 100, 2
        ),
    }


def main():
    print("Analyzing AntAWS 3-hourly dataset...\n")

    results = []

    with ZipFile(ZIP_PATH, "r") as zip_file:

        csv_files = [
            name
            for name in zip_file.namelist()
            if name.startswith("3_hourly/")
            and name.lower().endswith(".csv")
        ]

        print(f"Station files found: {len(csv_files)}\n")

        for index, csv_path in enumerate(csv_files, start=1):

            result = analyze_station(zip_file, csv_path)

            if result:
                results.append(result)

            if index % 25 == 0:
                print(f"Processed {index}/{len(csv_files)} stations...")

    summary = pd.DataFrame(results)

    summary = summary.sort_values(
        "complete_tprh",
        ascending=False
    )

    print("\n========== ANT AWS SUMMARY ==========\n")

    print(summary.head(20).to_string(index=False))

    print("\n=====================================\n")

    print(
        f"Stations successfully analyzed: {len(summary)}"
    )

    print(
        f"Total complete T+P+RH observations: "
        f"{summary['complete_tprh'].sum():,}"
    )

    output_path = Path("data/antaws_station_summary.csv")

    summary.to_csv(output_path, index=False)

    print(f"\nSummary saved to: {output_path}")


if __name__ == "__main__":
    main()