import requests
import json

URL = (
    "https://wis2box.imd.gov.in/oapi/collections/"
    "urn:wmo:md:in-imd:surface-based-observations.synop/items"
)

PARAMS = {
    "limit": 1000
}

print("Checking IMD observations for humidity...")

response = requests.get(
    URL,
    params=PARAMS,
    timeout=60,
    verify=False,
)

response.raise_for_status()

data = response.json()

features = data.get("features", [])

print(f"\nRecords received: {len(features)}")

humidity_records = []

for feature in features:
    properties = feature.get("properties", {})

    parameter = properties.get("name")

    if parameter and "humid" in parameter.lower():
        humidity_records.append({
            "station_id": properties.get("wigos_station_identifier"),
            "parameter": parameter,
            "value": properties.get("value"),
            "unit": properties.get("units"),
            "timestamp": properties.get("phenomenonTime"),
        })

print("\n========== HUMIDITY RESULTS ==========")

if humidity_records:
    print(f"Humidity records found: {len(humidity_records)}")

    for record in humidity_records[:20]:
        print(json.dumps(record, indent=2))

else:
    print("No humidity parameter found in this batch.")

print("\n======================================")