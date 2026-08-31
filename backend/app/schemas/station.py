from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StationResponse(BaseModel):
    id: int
    station_id: str
    name: str
    latitude: float | None = None
    longitude: float | None = None
    elevation: float | None = None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)