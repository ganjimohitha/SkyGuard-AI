import requests
import pandas as pd


URL = (
    "https://wis2box.imd.gov.in/oapi/collections/"
    "urn:wmo:md:in-imd:surface-based-observations.synop/items"
)

PARAMS = {
    "limit": 100
}


def fetch_observations():
    print("Downloading observations from IMD...")

    response = requests.get(
        URL,
        params=PARAMS,
        timeout=30,
        verify=False,
    )

    response.raise_for_status()

    return response.json()


def extract_records(data):
    records = []

    for feature in data.get("features", []):

        properties = feature.get("properties", {})
        geometry = feature.get("geometry") or {}

        coordinates = geometry.get("coordinates") or [None, None]

        longitude = coordinates[0] if len(coordinates) > 0 else None
        latitude = coordinates[1] if len(coordinates) > 1 else None

        records.append({
            "station_id": properties.get(
                "wigos_station_identifier"
            ),
            "timestamp": properties.get(
                "phenomenonTime"
            ),
            "parameter": properties.get(
                "name"
            ),
            "value": properties.get(
                "value"
            ),
            "unit": properties.get(
                "units"
            ),
            "latitude": latitude,
            "longitude": longitude,
        })

    return records


def main():

    data = fetch_observations()

    records = extract_records(data)

    df = pd.DataFrame(records)

    print("\n========== IMD DATA INSPECTION ==========")

    print(f"\nTotal records: {len(df)}")

    print(
        f"Unique stations: "
        f"{df['station_id'].nunique()}"
    )

    print("\nParameters found:")

    print(
        df["parameter"]
        .value_counts()
        .to_string()
    )

    print("\nUnits found:")

    print(
        df["unit"]
        .value_counts()
        .to_string()
    )

    print("\nSample records:")

    print(
        df.head(20)
        .to_string(index=False)
    )

    print("\n==========================================")


if __name__ == "__main__":
    main()