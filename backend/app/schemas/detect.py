from pydantic import BaseModel, Field


class SensorReading(BaseModel):
    temperature: float
    pressure: float
    humidity: float = Field(..., ge=0, le=100)


class SensorInput(BaseModel):
    temperature: float
    pressure: float
    humidity: float = Field(..., ge=0, le=100)

    station_id: str | None = None
    timestamp: str | None = None

    history: list[SensorReading] = Field(
        default_factory=list,
        description="Recent sensor readings in chronological order",
    )


class DetectionResponse(BaseModel):
    is_anomaly: bool
    anomaly_type: str
    anomaly_score: float
    confidence: float