from dataclasses import dataclass
from datetime import datetime


@dataclass
class FlightData:
    flight_no: str = None
    origin: str = None
    destination: str = None
    departure: datetime = None
    arrival: datetime = None
    base_price: int = None
    bag_price: int = None
    bags_allowed: int = None
