from fastapi import APIRouter

from app.schemas.detect import SensorInput, DetectionResponse
from app.services.anomaly_detector import detector


router = APIRouter(
    prefix="/detect",
    tags=["Anomaly Detection"],
)


@router.post(
    "",
    response_model=DetectionResponse,
)
def detect_anomaly(sensor: SensorInput):

    history = [
        reading.model_dump()
        for reading in sensor.history
    ]

    result = detector.predict(
        temperature=sensor.temperature,
        pressure=sensor.pressure,
        humidity=sensor.humidity,
        history=history,
    )

    return result