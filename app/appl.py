from fastapi import FastAPI, APIRouter, Query
from typing import Optional
from datetime import date
from pydantic import BaseModel, Field

router = APIRouter(prefix='/hotelss', tags=['hotelsss'])

hotels = [
    {
        'address': 'г. Москва, ул. Ленина, д. 1',
        'name': 'Отель Космос',
        'stars': 3,
    }
]


class BookingRequest(BaseModel):
    room_id: int = Field(example=1, title='ID комнаты')
    date_from: date = Field(example='2021-08-01', title='Дата начала бронирования')
    date_to: date = Field(example='2021-08-10', title='Дата окончания бронирования')


class BookingResponse(BaseModel):
    address: str
    name: str
    stars: int


@router.get('/{hotel_id}')
async def get_hotel_by_id(hotel_id: int, date_from, date_to):
    return {'hotel_id': hotel_id, 'date_from': date_from, 'date_to': date_to}


@router.get('/')
async def get_hotels_by_params(date_from: date,
                               date_to: date,
                               stars: Optional[int] = Query(None, ge=1, le=5),
                               has_spa: Optional[bool] = None,
                               location: Optional[str] = Query(None, min_length=3, max_length=50)) -> list[BookingResponse]:
    return {'date_from': date_from, 'date_to': date_to, 'location': location, 'stars': stars, 'has_spa': has_spa}





@router.post('/booking')
async def add_booking(booking_request: BookingRequest):
    return {'room_id': booking_request.room_id,
            'date_from': booking_request.date_from,
            'date_to': booking_request.date_to}