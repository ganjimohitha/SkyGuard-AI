from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.base import Base
from app.models.station import Station
from app.models.observation import Observation


INPUT_PATH = Path("data/processed/aws_features.csv")

BATCH_SIZE = 5000


def create_tables():
    from app.database.connection import engine

    Base.metadata.create_all(bind=engine)


def ingest_stations(
    db: Session,
    station_ids: list[str],
):
    existing = {
        station.station_id
        for station in db.query(Station).all()
    }

    new_stations = []

    for station_id in station_ids:
        if station_id not in existing:
            new_stations.append(
                Station(
                    station_id=station_id,
                    name=station_id,
                    status="active",
                )
            )

    if new_stations:
        db.add_all(new_stations)
        db.commit()

    print(f"Stations in database: {len(station_ids)}")


def ingest_observations(db: Session):
    print("Loading AWS observations...")

    df = pd.read_csv(
        INPUT_PATH,
        usecols=[
            "station_id",
            "timestamp",
            "temperature",
            "pressure",
            "humidity",
        ],
        parse_dates=["timestamp"],
    )

    print(f"Source observations: {len(df):,}")

    inserted = 0

    for start in range(0, len(df), BATCH_SIZE):
        batch = df.iloc[start:start + BATCH_SIZE]

        observations = [
            Observation(
                station_id=row.station_id,
                timestamp=row.timestamp.to_pydatetime().replace(
                    tzinfo=None
                ),
                temperature=float(row.temperature),
                pressure=float(row.pressure),
                humidity=float(row.humidity),
            )
            for row in batch.itertuples(index=False)
        ]

        db.add_all(observations)
        db.commit()

        inserted += len(observations)

        print(
            f"Inserted {inserted:,} / {len(df):,}"
        )

    return inserted


def main():
    print("========================================")
    print("SkyGuard AWS Observation Ingestion")
    print("========================================")

    create_tables()

    db = SessionLocal()

    try:
        station_ids = sorted(
            pd.read_csv(
                INPUT_PATH,
                usecols=["station_id"],
            )["station_id"]
            .dropna()
            .unique()
            .tolist()
        )

        ingest_stations(
            db,
            station_ids,
        )

        inserted = ingest_observations(db)

        print("\n========== INGESTION COMPLETE ==========")
        print(f"Stations:     {len(station_ids)}")
        print(f"Observations: {inserted:,}")

    finally:
        db.close()

    print("========================================")


if __name__ == "__main__":
    main()