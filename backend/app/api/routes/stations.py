from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.station import Station
from app.schemas.station import StationResponse
from app.services.observation_detector import observation_detector


router = APIRouter(
    prefix="/stations",
    tags=["Stations"],
)


@router.get(
    "",
    response_model=list[StationResponse],
)
def get_stations(
    db: Session = Depends(get_db),
):
    return (
        db.query(Station)
        .order_by(Station.name)
        .all()
    )


@router.get(
    "/{station_id}",
    response_model=StationResponse,
)
def get_station(
    station_id: str,
    db: Session = Depends(get_db),
):
    station = (
        db.query(Station)
        .filter(
            Station.station_id == station_id
        )
        .first()
    )

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found",
        )

    return station


@router.get(
    "/{station_id}/detect",
)
def detect_latest_station(
    station_id: str,
    db: Session = Depends(get_db),
):
    try:
        return observation_detector.detect_latest(
            db,
            station_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )