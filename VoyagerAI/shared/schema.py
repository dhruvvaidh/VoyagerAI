# voyagerai/shared/schema.py
from typing import List, Optional
from pydantic import BaseModel, Field


class FlightLeg(BaseModel):
    depart_airport: str
    arrive_airport: str
    depart_time: str   # ISO 8601
    arrive_time: str
    airline: str
    flight_number: str


class FlightInfo(BaseModel):
    outbound: FlightLeg
    return_: Optional[FlightLeg] = Field(None, alias="return")
    price: float
    booking_link: str


class AccommodationInfo(BaseModel):
    name: str
    check_in: str      # ISO 8601 date
    check_out: str
    price: float
    booking_link: Optional[str]


class DayPlan(BaseModel):
    day: int
    plan: str


class AggregatedTrip(BaseModel):
    flight_info: Optional[FlightInfo] = None
    accommodation_info: Optional[AccommodationInfo] = None
    itinerary_info: Optional[List[DayPlan]] = None