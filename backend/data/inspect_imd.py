import truststore

truststore.inject_into_ssl()

import json
import requests


URL = (
    "https://wis2box.imd.gov.in/oapi/collections/"
    "urn:wmo:md:in-imd:surface-based-observations.synop/items"
)

PARAMS = {
    "limit": 10
}


print("Connecting to IMD WIS2 API...")

response = requests.get(
    URL,
    params=PARAMS,
    timeout=30,
    verify=False,
)

response.raise_for_status()

data = response.json()

print("\nSuccessfully downloaded data.")

print("\nTop-level keys:")
print(list(data.keys()))

features = data.get("features", [])

print(f"\nNumber of features: {len(features)}")

if features:
    first_feature = features[0]

    print("\n========== FIRST FEATURE ==========")

    print(json.dumps(
        first_feature,
        indent=4,
        ensure_ascii=False
    ))

    print("\n========== PROPERTY KEYS ==========")

    properties = first_feature.get("properties", {})

    print(list(properties.keys()))

    print("\n========== PROPERTY VALUES ==========")

    for key, value in properties.items():
        print(f"{key}: {value}")

    print("\n====================================")
else:
    print("No features returned.")