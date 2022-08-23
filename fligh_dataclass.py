from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FlightData:
    flight_no: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    departure: Optional[datetime] = None
    arrival: Optional[datetime] = None
    base_price: Optional[int] = None
    bag_price: Optional[int] = None
    bags_allowed: Optional[int] = None
