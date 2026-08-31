from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.observation import Observation
from app.models.station import Station
from app.schemas.observation import ObservationResponse


router = APIRouter(
    prefix="/stations",
    tags=["Observations"],
)


@router.get(
    "/{station_id}/observations",
    response_model=list[ObservationResponse],
)
def get_station_observations(
    station_id: str,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    station = (
        db.query(Station)
        .filter(Station.station_id == station_id)
        .first()
    )

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found",
        )

    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 1000",
        )

    return (
        db.query(Observation)
        .filter(Observation.station_id == station_id)
        .order_by(Observation.timestamp.desc())
        .limit(limit)
        .all()
    )


@router.get(
    "/{station_id}/observations/latest",
    response_model=ObservationResponse,
)
def get_latest_observation(
    station_id: str,
    db: Session = Depends(get_db),
):
    station = (
        db.query(Station)
        .filter(Station.station_id == station_id)
        .first()
    )

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found",
        )

    observation = (
        db.query(Observation)
        .filter(Observation.station_id == station_id)
        .order_by(Observation.timestamp.desc())
        .first()
    )

    if observation is None:
        raise HTTPException(
            status_code=404,
            detail="No observations found for station",
        )

    return observation