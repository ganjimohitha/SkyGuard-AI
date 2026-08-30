from pathlib import Path

import joblib
import numpy as np
import pandas as pd


MODEL_PATH = Path("models/isolation_forest.joblib")


class AnomalyDetector:

    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Isolation Forest model not found: {MODEL_PATH}"
            )

        model_data = joblib.load(MODEL_PATH)

        if not isinstance(model_data, dict):
            raise ValueError(
                "Invalid model format. Expected a dictionary."
            )

        self.model = model_data["model"]
        self.features = model_data["features"]

    # ---------------------------------------------------------
    # Statistical detection
    # ---------------------------------------------------------

    def predict_statistical(
        self,
        temperature: float,
        pressure: float,
        humidity: float,
    ) -> dict:

        data = {
            "temperature": temperature,
            "pressure": pressure,
            "humidity": humidity,
            "hour": 12,
            "month": 1,
            "day_of_year": 1,
            "month_sin": 0.0,
            "month_cos": 1.0,
            "hour_sin": 0.0,
            "hour_cos": -1.0,
            "temperature_diff": 0.0,
            "temperature_diff_abs": 0.0,
            "pressure_diff": 0.0,
            "pressure_diff_abs": 0.0,
            "humidity_diff": 0.0,
            "humidity_diff_abs": 0.0,
            "temperature_rolling_mean": temperature,
            "temperature_rolling_std": 0.0,
            "temperature_deviation": 0.0,
            "pressure_rolling_mean": pressure,
            "pressure_rolling_std": 0.0,
            "pressure_deviation": 0.0,
            "humidity_rolling_mean": humidity,
            "humidity_rolling_std": 0.0,
            "humidity_deviation": 0.0,
            "temperature_humidity_interaction": temperature * humidity,
            "original_temperature": temperature,
            "original_pressure": pressure,
            "original_humidity": humidity,
        }

        X = pd.DataFrame([data])
        X = X[self.features]

        prediction = int(self.model.predict(X)[0])

        decision_score = float(
            self.model.decision_function(X)[0]
        )

        is_anomaly = prediction == -1

        anomaly_score = max(
            0.0,
            min(1.0, 0.5 - decision_score)
        )

        confidence = max(
            0.0,
            min(1.0, anomaly_score * 2.0)
        )

        return {
            "is_anomaly": is_anomaly,
            "anomaly_type": (
                "statistical_anomaly"
                if is_anomaly
                else "normal"
            ),
            "anomaly_score": round(anomaly_score, 4),
            "confidence": round(confidence, 4),
        }

    # ---------------------------------------------------------
    # Frozen sensor detection
    # ---------------------------------------------------------

    @staticmethod
    def detect_frozen_sensor(history: list) -> bool:

        if len(history) < 8:
            return False

        temperatures = np.array(
            [reading["temperature"] for reading in history[-8:]],
            dtype=float,
        )

        if np.std(temperatures, ddof=1) > 0.05:
            return False

        if abs(temperatures[-1] - temperatures[-2]) > 0.05:
            return False

        return True

    # ---------------------------------------------------------
    # Temperature drift detection
    # ---------------------------------------------------------

    @staticmethod
    def detect_temperature_drift(history: list) -> bool:

        if len(history) < 8:
            return False

        temperatures = np.array(
            [reading["temperature"] for reading in history[-8:]],
            dtype=float,
        )

        differences = np.diff(temperatures)

        if len(differences) < 7:
            return False

        rolling_change = differences.sum()

        return abs(rolling_change) >= 14.0

    # ---------------------------------------------------------
    # Combined prediction
    # ---------------------------------------------------------

    def predict(
        self,
        temperature: float,
        pressure: float,
        humidity: float,
        history: list | None = None,
    ) -> dict:

        history = history or []

        current = {
            "temperature": temperature,
            "pressure": pressure,
            "humidity": humidity,
        }

        full_history = history + [current]

        statistical = self.predict_statistical(
            temperature,
            pressure,
            humidity,
        )

        frozen = self.detect_frozen_sensor(
            full_history
        )

        drift = self.detect_temperature_drift(
            full_history
        )

        if frozen:
            return {
                "is_anomaly": True,
                "anomaly_type": "frozen_sensor",
                "anomaly_score": 1.0,
                "confidence": 0.99,
            }

        if drift:
            return {
                "is_anomaly": True,
                "anomaly_type": "temperature_drift",
                "anomaly_score": 0.9,
                "confidence": 0.9,
            }

        return statistical


detector = AnomalyDetector()