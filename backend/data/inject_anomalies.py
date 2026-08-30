# from pathlib import Path

# import numpy as np
# import pandas as pd


# INPUT_PATH = Path("data/processed/aws_features.csv")
# OUTPUT_PATH = Path("data/processed/aws_anomaly_dataset.csv")

# RANDOM_SEED = 42
# ANOMALY_RATE = 0.05

# # Dataset is 3-hourly.
# # 8 observations = approximately 24 hours.
# TEMPORAL_WINDOW = 8


# def main():

#     print("Starting SkyGuard anomaly injection...\n")

#     np.random.seed(RANDOM_SEED)

#     # ---------------------------------------------------------
#     # Load dataset
#     # ---------------------------------------------------------

#     df = pd.read_csv(
#         INPUT_PATH,
#         parse_dates=["timestamp"]
#     )

#     print(f"Input observations: {len(df):,}")

#     df = (
#         df.sort_values(
#             ["station_id", "timestamp"]
#         )
#         .reset_index(drop=True)
#     )

#     # ---------------------------------------------------------
#     # Preserve original measurements
#     # ---------------------------------------------------------

#     for column in [
#         "temperature",
#         "pressure",
#         "humidity"
#     ]:
#         df[f"original_{column}"] = df[column]

#     # ---------------------------------------------------------
#     # Ground truth
#     # ---------------------------------------------------------

#     df["is_anomaly"] = 0
#     df["anomaly_type"] = "normal"

#     # ---------------------------------------------------------
#     # Create station index lookup
#     # ---------------------------------------------------------

#     station_indices = {
#         station: group.index.to_numpy()
#         for station, group in df.groupby("station_id")
#     }

#     # ---------------------------------------------------------
#     # Select anomaly seeds
#     # ---------------------------------------------------------

#     number_of_anomalies = int(
#         len(df) * ANOMALY_RATE
#     )

#     valid_indices = []

#     for indices in station_indices.values():

#         if len(indices) > TEMPORAL_WINDOW:

#             valid_indices.extend(
#                 indices[TEMPORAL_WINDOW:]
#             )

#     valid_indices = np.asarray(valid_indices)

#     anomaly_indices = np.random.choice(
#         valid_indices,
#         size=number_of_anomalies,
#         replace=False
#     )

#     anomaly_types = [
#         "temperature_spike",
#         "pressure_spike",
#         "humidity_spike",
#         "frozen_sensor",
#         "temperature_drift",
#         "multivariate_inconsistency",
#     ]

#     assigned_types = np.random.choice(
#         anomaly_types,
#         size=number_of_anomalies,
#         replace=True
#     )

#     anomaly_map = dict(
#         zip(
#             anomaly_indices,
#             assigned_types
#         )
#     )

#     # ---------------------------------------------------------
#     # Simple point anomalies
#     # ---------------------------------------------------------

#     point_masks = {}

#     for anomaly_type in [
#         "temperature_spike",
#         "pressure_spike",
#         "humidity_spike",
#         "multivariate_inconsistency"
#     ]:

#         indices = np.asarray([
#             index
#             for index, kind in anomaly_map.items()
#             if kind == anomaly_type
#         ])

#         point_masks[anomaly_type] = indices

#     # Temperature spike
#     indices = point_masks["temperature_spike"]

#     df.loc[
#         indices,
#         "temperature"
#     ] += 60.0

#     df.loc[
#         indices,
#         "is_anomaly"
#     ] = 1

#     df.loc[
#         indices,
#         "anomaly_type"
#     ] = "temperature_spike"

#     # Pressure spike
#     indices = point_masks["pressure_spike"]

#     df.loc[
#         indices,
#         "pressure"
#     ] -= 250.0

#     df.loc[
#         indices,
#         "is_anomaly"
#     ] = 1

#     df.loc[
#         indices,
#         "anomaly_type"
#     ] = "pressure_spike"

#     # Humidity spike
#     indices = point_masks["humidity_spike"]

#     df.loc[
#         indices,
#         "humidity"
#     ] = 150.0

#     df.loc[
#         indices,
#         "is_anomaly"
#     ] = 1

#     df.loc[
#         indices,
#         "anomaly_type"
#     ] = "humidity_spike"

#     # Multivariate inconsistency
#     indices = point_masks[
#         "multivariate_inconsistency"
#     ]

#     df.loc[
#         indices,
#         "temperature"
#     ] += 35.0

#     df.loc[
#         indices,
#         "is_anomaly"
#     ] = 1

#     df.loc[
#         indices,
#         "anomaly_type"
#     ] = "multivariate_inconsistency"

#     # ---------------------------------------------------------
#     # Temporal anomalies
#     # ---------------------------------------------------------

#     frozen_seed_indices = [
#         index
#         for index, kind in anomaly_map.items()
#         if kind == "frozen_sensor"
#     ]

#     drift_seed_indices = [
#         index
#         for index, kind in anomaly_map.items()
#         if kind == "temperature_drift"
#     ]

#     # =========================================================
#     # FROZEN SENSOR
#     # =========================================================

#     print(
#         f"\nInjecting frozen sensor sequences: "
#         f"{len(frozen_seed_indices):,}"
#     )

#     for seed_index in frozen_seed_indices:

#         station = df.at[
#             seed_index,
#             "station_id"
#         ]

#         indices = station_indices[station]

#         position = np.searchsorted(
#             indices,
#             seed_index
#         )

#         if position < TEMPORAL_WINDOW:
#             continue

#         window_indices = indices[
#             position - TEMPORAL_WINDOW + 1:
#             position + 1
#         ]

#         source_index = indices[
#             position - TEMPORAL_WINDOW
#         ]

#         frozen_value = df.at[
#             source_index,
#             "temperature"
#         ]

#         df.loc[
#             window_indices,
#             "temperature"
#         ] = frozen_value

#         df.loc[
#             window_indices,
#             "is_anomaly"
#         ] = 1

#         df.loc[
#             window_indices,
#             "anomaly_type"
#         ] = "frozen_sensor"

#     # =========================================================
#     # TEMPERATURE DRIFT
#     # =========================================================

#     print(
#         f"Injecting temperature drift sequences: "
#         f"{len(drift_seed_indices):,}"
#     )

#     for seed_index in drift_seed_indices:

#         station = df.at[
#             seed_index,
#             "station_id"
#         ]

#         indices = station_indices[station]

#         position = np.searchsorted(
#             indices,
#             seed_index
#         )

#         if position < TEMPORAL_WINDOW:
#             continue

#         window_indices = indices[
#             position - TEMPORAL_WINDOW + 1:
#             position + 1
#         ]

#         drift_values = np.linspace(
#             0.0,
#             14.0,
#             len(window_indices)
#         )

#         df.loc[
#             window_indices,
#             "temperature"
#         ] += drift_values

#         df.loc[
#             window_indices,
#             "is_anomaly"
#         ] = 1

#         df.loc[
#             window_indices,
#             "anomaly_type"
#         ] = "temperature_drift"

#     # ---------------------------------------------------------
#     # Recalculate difference features
#     # ---------------------------------------------------------

#     print("\nRecalculating difference features...")

#     for column in [
#         "temperature",
#         "pressure",
#         "humidity"
#     ]:

#         diff = (
#             df.groupby("station_id")[column]
#             .diff()
#         )

#         df[f"{column}_diff"] = diff
#         df[f"{column}_diff_abs"] = diff.abs()

#     difference_columns = [
#         "temperature_diff",
#         "temperature_diff_abs",
#         "pressure_diff",
#         "pressure_diff_abs",
#         "humidity_diff",
#         "humidity_diff_abs",
#     ]

#     df[difference_columns] = (
#         df[difference_columns]
#         .fillna(0)
#     )

#     # ---------------------------------------------------------
#     # Save
#     # ---------------------------------------------------------

#     print("\nSaving anomaly dataset...")

#     df.to_csv(
#         OUTPUT_PATH,
#         index=False
#     )

#     # ---------------------------------------------------------
#     # Results
#     # ---------------------------------------------------------

#     print("\n========== INJECTION RESULTS ==========")

#     print(
#         f"Total observations: "
#         f"{len(df):,}"
#     )

#     print(
#         f"Anomalous observations: "
#         f"{df['is_anomaly'].sum():,}"
#     )

#     print(
#         f"Actual anomaly rate: "
#         f"{df['is_anomaly'].mean() * 100:.2f}%"
#     )

#     print("\nAnomaly distribution:")

#     print(
#         df.loc[
#             df["is_anomaly"] == 1,
#             "anomaly_type"
#         ]
#         .value_counts()
#         .to_string()
#     )

#     print("\nLabels:")

#     print(
#         df["is_anomaly"]
#         .value_counts()
#         .sort_index()
#         .to_string()
#     )

#     print("\nMissing values:")

#     missing = (
#         df.isna()
#         .sum()
#         .loc[lambda x: x > 0]
#     )

#     if len(missing) == 0:
#         print("None")
#     else:
#         print(missing.to_string())

#     print("\nSaved to:")
#     print(OUTPUT_PATH)

#     print("========================================")


# if __name__ == "__main__":
#     main()

from pathlib import Path

import numpy as np
import pandas as pd


INPUT_PATH = Path("data/processed/aws_features.csv")
OUTPUT_PATH = Path("data/processed/aws_anomaly_dataset.csv")

RANDOM_SEED = 42
ANOMALY_RATE = 0.05

# Dataset is 3-hourly.
# 8 observations = 24 hours.
TEMPORAL_WINDOW = 8

# Fraction of anomaly budget assigned to each category.
# Temporal anomalies consume 8 rows per sequence.
ANOMALY_TYPE_WEIGHTS = {
    "temperature_spike": 0.15,
    "pressure_spike": 0.15,
    "humidity_spike": 0.15,
    "multivariate_inconsistency": 0.15,
    "frozen_sensor": 0.20,
    "temperature_drift": 0.20,
}


def main():

    print("Starting SkyGuard anomaly injection...\n")

    np.random.seed(RANDOM_SEED)

    # ---------------------------------------------------------
    # Load dataset
    # ---------------------------------------------------------

    df = pd.read_csv(
        INPUT_PATH,
        parse_dates=["timestamp"]
    )

    print(f"Input observations: {len(df):,}")

    df = (
        df.sort_values(
            ["station_id", "timestamp"]
        )
        .reset_index(drop=True)
    )

    # ---------------------------------------------------------
    # Preserve original measurements
    # ---------------------------------------------------------

    for column in [
        "temperature",
        "pressure",
        "humidity"
    ]:
        df[f"original_{column}"] = df[column]

    # ---------------------------------------------------------
    # Ground truth
    # ---------------------------------------------------------

    df["is_anomaly"] = 0
    df["anomaly_type"] = "normal"

    # ---------------------------------------------------------
    # Final anomaly budget
    # ---------------------------------------------------------

    anomaly_budget = int(
        len(df) * ANOMALY_RATE
    )

    print(
        f"Target anomalous observations: "
        f"{anomaly_budget:,}"
    )

    # ---------------------------------------------------------
    # Station index lookup
    # ---------------------------------------------------------

    station_indices = {
        station: group.index.to_numpy()
        for station, group in df.groupby("station_id")
    }

    # ---------------------------------------------------------
    # Select non-overlapping temporal windows
    # ---------------------------------------------------------

    temporal_budget = int(
        anomaly_budget
        * (
            ANOMALY_TYPE_WEIGHTS["frozen_sensor"]
            + ANOMALY_TYPE_WEIGHTS["temperature_drift"]
        )
    )

    temporal_sequence_count = (
        temporal_budget // TEMPORAL_WINDOW
    )

    candidate_windows = []

    for station, indices in station_indices.items():

        # Need enough previous observations.
        if len(indices) < TEMPORAL_WINDOW:
            continue

        for position in range(
            TEMPORAL_WINDOW - 1,
            len(indices)
        ):

            window = indices[
                position - TEMPORAL_WINDOW + 1:
                position + 1
            ]

            candidate_windows.append(
                (station, window)
            )

    np.random.shuffle(candidate_windows)

    selected_windows = []

    used_indices = set()

    for station, window in candidate_windows:

        window_set = set(window)

        # Ensure temporal sequences do not overlap.
        if used_indices.intersection(window_set):
            continue

        selected_windows.append(
            (station, window)
        )

        used_indices.update(window_set)

        if len(selected_windows) >= temporal_sequence_count:
            break

    # Split temporal sequences between frozen/drift.
    frozen_count = (
        temporal_sequence_count // 2
    )

    drift_count = (
        temporal_sequence_count
        - frozen_count
    )

    frozen_windows = selected_windows[
        :frozen_count
    ]

    drift_windows = selected_windows[
        frozen_count:
    ]

    # ---------------------------------------------------------
    # Inject frozen sensors
    # ---------------------------------------------------------

    print(
        f"Frozen sensor sequences: "
        f"{len(frozen_windows):,}"
    )

    for station, window in frozen_windows:

        first_index = window[0]

        # Use the observation immediately before
        # the anomalous sequence as the frozen value.
        indices = station_indices[station]

        position = np.searchsorted(
            indices,
            first_index
        )

        if position == 0:
            continue

        source_index = indices[position - 1]

        frozen_value = df.at[
            source_index,
            "temperature"
        ]

        df.loc[
            window,
            "temperature"
        ] = frozen_value

        df.loc[
            window,
            "is_anomaly"
        ] = 1

        df.loc[
            window,
            "anomaly_type"
        ] = "frozen_sensor"

    # ---------------------------------------------------------
    # Inject temperature drift
    # ---------------------------------------------------------

    print(
        f"Temperature drift sequences: "
        f"{len(drift_windows):,}"
    )

    for station, window in drift_windows:

        drift_values = np.linspace(
            0.0,
            14.0,
            TEMPORAL_WINDOW
        )

        df.loc[
            window,
            "temperature"
        ] += drift_values

        df.loc[
            window,
            "is_anomaly"
        ] = 1

        df.loc[
            window,
            "anomaly_type"
        ] = "temperature_drift"

    # ---------------------------------------------------------
    # Remaining anomaly budget for point anomalies
    # ---------------------------------------------------------

    temporal_rows = (
        len(frozen_windows)
        + len(drift_windows)
    ) * TEMPORAL_WINDOW

    remaining_budget = (
        anomaly_budget - temporal_rows
    )

    print(
        f"Temporal anomaly observations: "
        f"{temporal_rows:,}"
    )

    print(
        f"Remaining point-anomaly budget: "
        f"{remaining_budget:,}"
    )

    # ---------------------------------------------------------
    # Select point anomaly rows
    # ---------------------------------------------------------

    available_indices = np.array([
        index
        for index in df.index
        if index not in used_indices
    ])

    point_indices = np.random.choice(
        available_indices,
        size=remaining_budget,
        replace=False
    )

    point_types = [
        "temperature_spike",
        "pressure_spike",
        "humidity_spike",
        "multivariate_inconsistency",
    ]

    assigned_types = np.random.choice(
        point_types,
        size=remaining_budget,
        replace=True
    )

    # ---------------------------------------------------------
    # Inject point anomalies
    # ---------------------------------------------------------

    for index, anomaly_type in zip(
        point_indices,
        assigned_types
    ):

        if anomaly_type == "temperature_spike":

            df.at[
                index,
                "temperature"
            ] += 60.0

        elif anomaly_type == "pressure_spike":

            df.at[
                index,
                "pressure"
            ] -= 250.0

        elif anomaly_type == "humidity_spike":

            df.at[
                index,
                "humidity"
            ] = 150.0

        elif anomaly_type == "multivariate_inconsistency":

            df.at[
                index,
                "temperature"
            ] += 35.0

        df.at[
            index,
            "is_anomaly"
        ] = 1

        df.at[
            index,
            "anomaly_type"
        ] = anomaly_type

    # ---------------------------------------------------------
    # Recalculate difference features
    # ---------------------------------------------------------

    print(
        "\nRecalculating difference features..."
    )

    for column in [
        "temperature",
        "pressure",
        "humidity"
    ]:

        diff = (
            df.groupby("station_id")[column]
            .diff()
        )

        df[f"{column}_diff"] = diff
        df[f"{column}_diff_abs"] = diff.abs()

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

    print(
        "\nSaving anomaly dataset..."
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    # ---------------------------------------------------------
    # Results
    # ---------------------------------------------------------

    print(
        "\n========== INJECTION RESULTS =========="
    )

    print(
        f"Total observations: "
        f"{len(df):,}"
    )

    print(
        f"Anomalous observations: "
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

    missing = (
        df.isna()
        .sum()
        .loc[lambda x: x > 0]
    )

    if len(missing) == 0:
        print("None")
    else:
        print(missing.to_string())

    print("\nSaved to:")
    print(OUTPUT_PATH)

    print("========================================")


if __name__ == "__main__":
    main()