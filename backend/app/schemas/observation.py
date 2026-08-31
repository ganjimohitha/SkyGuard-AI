from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ObservationResponse(BaseModel):
    id: int
    station_id: str
    timestamp: datetime
    temperature: float
    pressure: float
    humidity: float

    model_config = ConfigDict(from_attributes=True)