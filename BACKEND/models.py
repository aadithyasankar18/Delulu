from pydantic import BaseModel

class UserSignup(BaseModel):
    name: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class EventCreate(BaseModel):
    title: str
    seatsAvailable: int
    priceRegular: int
    priceVIP: int

class BookingCreate(BaseModel):
    user_id: str
    event_id: str
    seatsBooked: int
    seatType: str