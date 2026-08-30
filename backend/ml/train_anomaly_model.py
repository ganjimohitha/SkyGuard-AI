import os
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)


# ============================================================
# PATHS
# ============================================================

INPUT_PATH = "data/processed/aws_anomaly_dataset.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "isolation_forest.joblib")


# ============================================================
# CONFIGURATION
# ============================================================

RANDOM_STATE = 42
CONTAMINATION = 0.05

# Use 80% of the observations for training and 20% for testing.
TRAIN_RATIO = 0.80


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    print("Loading SkyGuard anomaly dataset...")

    df = pd.read_csv(INPUT_PATH)

    print(f"Total rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    return df


# ============================================================
# SELECT FEATURES
# ============================================================

def select_features(df):
    """
    Select numeric ML features.

    We deliberately exclude:
      - timestamp
      - station_id
      - anomaly_type
      - is_anomaly

    The anomaly labels are ground truth for evaluation only.
    """

    excluded_columns = {
        "timestamp",
        "station_id",
        "anomaly_type",
        "is_anomaly",
    }

    feature_columns = [
        column
        for column in df.columns
        if column not in excluded_columns
        and pd.api.types.is_numeric_dtype(df[column])
    ]

    if not feature_columns:
        raise ValueError("No numeric ML features were found.")

    print("\n========== FEATURES ==========")
    print(f"Number of features: {len(feature_columns)}")

    for column in feature_columns:
        print(f"  - {column}")

    return feature_columns


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

def split_data(df, feature_columns):
    """
    Chronological split.

    This is important for time-series data:
    we train on earlier observations and evaluate on later
    observations instead of randomly mixing the timeline.
    """

    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

    df = df.sort_values("timestamp").reset_index(drop=True)

    split_index = int(len(df) * TRAIN_RATIO)

    train_df = df.iloc[:split_index].copy()
    test_df = df.iloc[split_index:].copy()

    X_train = train_df[feature_columns]
    X_test = test_df[feature_columns]

    y_test = test_df["is_anomaly"].astype(int)

    print("\n========== DATA SPLIT ==========")
    print(f"Training rows: {len(train_df):,}")
    print(f"Testing rows:  {len(test_df):,}")

    print("\nTraining time range:")
    print(f"  {train_df['timestamp'].min()}")
    print(f"  {train_df['timestamp'].max()}")

    print("\nTesting time range:")
    print(f"  {test_df['timestamp'].min()}")
    print(f"  {test_df['timestamp'].max()}")

    print("\nTest labels:")
    print(y_test.value_counts().sort_index())

    return X_train, X_test, y_test


# ============================================================
# TRAIN MODEL
# ============================================================

def train_model(X_train):
    print("\n========== TRAINING ==========")

    print("Training Isolation Forest...")

    model = IsolationForest(
        n_estimators=300,
        contamination=CONTAMINATION,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    model.fit(X_train)

    print("Training complete.")

    return model


# ============================================================
# EVALUATE MODEL
# ============================================================

def evaluate_model(model, X_test, y_test):
    print("\n========== EVALUATION ==========")

    predictions = model.predict(X_test)

    # Isolation Forest:
    #   1  = normal
    #  -1  = anomaly
    #
    # Convert to:
    #   0 = normal
    #   1 = anomaly

    y_pred = (predictions == -1).astype(int)

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    print("\nDetection Metrics:")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=["Normal", "Anomaly"],
            zero_division=0,
        )
    )

    print("\nPredicted distribution:")
    print(
        pd.Series(y_pred)
        .value_counts()
        .sort_index()
        .rename(index={0: "Normal", 1: "Anomaly"})
    )

    return y_pred


# ============================================================
# SAVE MODEL
# ============================================================

def save_model(model, feature_columns):
    os.makedirs(MODEL_DIR, exist_ok=True)

    model_package = {
        "model": model,
        "features": feature_columns,
        "contamination": CONTAMINATION,
        "random_state": RANDOM_STATE,
    }

    joblib.dump(model_package, MODEL_PATH)

    print("\n========== MODEL SAVED ==========")
    print(f"Saved to: {MODEL_PATH}")


# ============================================================
# MAIN
# ============================================================

def main():
    print("========================================")
    print("SkyGuard Isolation Forest Training")
    print("========================================")

    df = load_data()

    feature_columns = select_features(df)

    X_train, X_test, y_test = split_data(
        df,
        feature_columns,
    )

    model = train_model(X_train)

    evaluate_model(
        model,
        X_test,
        y_test,
    )

    save_model(
        model,
        feature_columns,
    )

    print("\n========================================")
    print("Training pipeline complete.")
    print("========================================")


if __name__ == "__main__":
    main()