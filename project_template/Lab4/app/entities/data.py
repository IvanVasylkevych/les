from datetime import datetime
from pydantic import BaseModel, field_validator
from app.entities.agent_data import AccelerometerData
from app.entities.agent_data import GpsData

class ParkingData(BaseModel):
    empty_count: float
    gps: GpsData

class Data(BaseModel):
    accelerometer: AccelerometerData
    gps: GpsData
    parking: ParkingData
    timestamp: datetime

    @classmethod
    @field_validator("timestamp", mode="before")
    def parse_timestamp(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError("Invalid timestamp format. Expected ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).")
