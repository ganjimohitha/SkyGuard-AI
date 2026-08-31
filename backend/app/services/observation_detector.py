from sqlalchemy.orm import Session

from app.models.observation import Observation
from app.models.station import Station
from app.services.anomaly_detector import detector


class ObservationDetector:

    @staticmethod
    def detect_latest(
        db: Session,
        station_id: str,
    ) -> dict:

        station = (
            db.query(Station)
            .filter(
                Station.station_id == station_id
            )
            .first()
        )

        if station is None:
            raise ValueError(
                f"Station not found: {station_id}"
            )

        observations = (
            db.query(Observation)
            .filter(
                Observation.station_id == station_id
            )
            .order_by(
                Observation.timestamp.desc()
            )
            .limit(8)
            .all()
        )

        if not observations:
            raise ValueError(
                f"No observations found for station: {station_id}"
            )

        observations = list(
            reversed(observations)
        )

        current = observations[-1]

        history = [
            {
                "temperature": observation.temperature,
                "pressure": observation.pressure,
                "humidity": observation.humidity,
            }
            for observation in observations[:-1]
        ]

        result = detector.predict(
            temperature=current.temperature,
            pressure=current.pressure,
            humidity=current.humidity,
            history=history,
        )

        return {
            "station_id": current.station_id,
            "timestamp": current.timestamp,
            "temperature": current.temperature,
            "pressure": current.pressure,
            "humidity": current.humidity,
            **result,
        }


observation_detector = ObservationDetector()