import joblib
import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
)


# ============================================================
# PATHS
# ============================================================

DATA_PATH = "data/processed/aws_anomaly_dataset.csv"
MODEL_PATH = "models/isolation_forest.joblib"

TRAIN_RATIO = 0.80


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    print("Loading SkyGuard anomaly dataset...")

    df = pd.read_csv(DATA_PATH)

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True,
    )

    df = df.sort_values("timestamp").reset_index(drop=True)

    print(f"Total rows: {len(df):,}")

    return df


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():
    print("Loading Isolation Forest model...")

    package = joblib.load(MODEL_PATH)

    model = package["model"]
    features = package["features"]

    print(f"Features used by model: {len(features)}")

    return model, features


# ============================================================
# CREATE TEST SET
# ============================================================

def create_test_set(df):
    split_index = int(len(df) * TRAIN_RATIO)

    test_df = df.iloc[split_index:].copy()

    print("\n========== TEST SET ==========")
    print(f"Test rows: {len(test_df):,}")
    print(
        f"Test period: "
        f"{test_df['timestamp'].min()} → "
        f"{test_df['timestamp'].max()}"
    )

    return test_df


# ============================================================
# PREDICT
# ============================================================

def predict(model, test_df, features):
    X_test = test_df[features]

    predictions = model.predict(X_test)

    # Isolation Forest:
    #  1  = normal
    # -1  = anomaly

    test_df = test_df.copy()

    test_df["predicted_anomaly"] = (
        predictions == -1
    ).astype(int)

    return test_df


# ============================================================
# OVERALL PERFORMANCE
# ============================================================

def print_overall_performance(df):
    y_true = df["is_anomaly"].astype(int)
    y_pred = df["predicted_anomaly"].astype(int)

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    print("\n========== OVERALL PERFORMANCE ==========")

    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")


# ============================================================
# PERFORMANCE BY ANOMALY TYPE
# ============================================================

def evaluate_anomaly_types(df):
    print("\n========== ANOMALY TYPE PERFORMANCE ==========")

    anomaly_types = sorted(
        df.loc[
            df["is_anomaly"] == 1,
            "anomaly_type",
        ]
        .dropna()
        .unique()
    )

    results = []

    for anomaly_type in anomaly_types:

        # Ground truth:
        # this particular anomaly type = positive
        y_true = (
            df["anomaly_type"] == anomaly_type
        ).astype(int)

        # Prediction:
        # model predicted anomaly = positive
        y_pred = df["predicted_anomaly"].astype(int)

        precision = precision_score(
            y_true,
            y_pred,
            zero_division=0,
        )

        recall = recall_score(
            y_true,
            y_pred,
            zero_division=0,
        )

        f1 = f1_score(
            y_true,
            y_pred,
            zero_division=0,
        )

        actual_count = int(y_true.sum())
        detected_count = int(
            ((y_true == 1) & (y_pred == 1)).sum()
        )

        results.append(
            {
                "anomaly_type": anomaly_type,
                "actual": actual_count,
                "detected": detected_count,
                "precision": precision,
                "recall": recall,
                "f1": f1,
            }
        )

    results_df = pd.DataFrame(results)

    if not results_df.empty:
        results_df = results_df.sort_values(
            "f1",
            ascending=False,
        )

    print(
        results_df.to_string(
            index=False,
            formatters={
                "precision": "{:.4f}".format,
                "recall": "{:.4f}".format,
                "f1": "{:.4f}".format,
            },
        )

    )

    return results_df


# ============================================================
# ANOMALY COUNTS
# ============================================================

def print_anomaly_counts(df):
    print("\n========== ANOMALY COUNTS ==========")

    actual = (
        df[df["is_anomaly"] == 1]
        ["anomaly_type"]
        .value_counts()
    )

    detected = (
        df[df["predicted_anomaly"] == 1]
        ["anomaly_type"]
        .value_counts()
    )

    counts = pd.DataFrame(
        {
            "actual": actual,
            "detected": detected,
        }
    ).fillna(0)

    counts["actual"] = counts["actual"].astype(int)
    counts["detected"] = counts["detected"].astype(int)

    print(counts)


# ============================================================
# MAIN
# ============================================================

def main():

    print("========================================")
    print("SkyGuard Anomaly Type Evaluation")
    print("========================================")

    df = load_data()

    model, features = load_model()

    test_df = create_test_set(df)

    test_df = predict(
        model,
        test_df,
        features,
    )

    print_overall_performance(test_df)

    results = evaluate_anomaly_types(
        test_df
    )

    print_anomaly_counts(
        test_df
    )

    print("\n========================================")
    print("Evaluation complete.")
    print("========================================")


if __name__ == "__main__":
    main()