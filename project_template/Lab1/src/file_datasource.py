from csv import reader
from datetime import datetime

from domain.parking import Parking
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps

class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.cache_data = {}

    def read(self) -> AggregatedData:
        data_points = (
            ("accelerometer", self.cache_data.get("accelerometer")),
            ("gps", self.cache_data.get("gps")),
            ("parking", self.cache_data.get("parking")),
        )

        processed_data = {}
        for data_type, raw_data in data_points:
            if raw_data is None:
                raise ValueError(f"Missing data for type: {data_type}")

            processed_data[data_type] = next(reader(raw_data))

        try:
            x, y, z = map(int, processed_data["accelerometer"])
        except ValueError:
            raise ValueError("Invalid accelerometer data format (must be integers)")

        try:
            longitude, latitude = map(float, processed_data["gps"])
        except ValueError:
            raise ValueError("Invalid GPS data format (must be floats)")

        try:
            empty_count = int(processed_data["parking"][0])
        except (IndexError, ValueError):
            raise ValueError("Invalid parking data format (must be a single integer)")

        accelerometer_obj = Accelerometer(x=x, y=y, z=z)
        gps_obj = Gps(longitude=longitude, latitude=latitude)
        parking_obj = Parking(empty_count=empty_count, gps=gps_obj)

        return AggregatedData(
            accelerometer=accelerometer_obj,
            gps=gps_obj,
            parking=parking_obj,
            timestamp=datetime.now()
        )

    def startReading(self, *args, **kwargs):
        self.cache_data["accelerometer"] = open(self.accelerometer_filename, 'r')
        self.cache_data["gps"] = open(self.gps_filename, 'r')
        self.cache_data["parking"] = open(self.parking_filename, 'r')

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        # This one is redundant for now as the reading is infinite
        pass