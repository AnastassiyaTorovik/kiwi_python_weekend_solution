from dataclasses import dataclass
from typing import Optional, Any, Union
from datetime import datetime


@dataclass
class FlightData:
    flight_no: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    departure: Optional[Union[str, datetime]] = None
    arrival: Optional[Union[str, datetime]] = None
    base_price: Optional[int] = None
    bag_price: Optional[int] = None
    bags_allowed: Optional[dataclass] = None
    parent: Optional[Any] = None

    def __post_init__(self):
        try:
            self.departure = datetime.strptime(self.departure, '%Y-%m-%dT%H:%M:%S')
            self.arrival = datetime.strptime(self.arrival, '%Y-%m-%dT%H:%M:%S')
        except Exception as e:
            raise ValueError(f"The departure and arrival should be in datetime format: {e}")

