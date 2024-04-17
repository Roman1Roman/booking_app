from datetime import date
from app.exceptions import HotelNotFound
from fastapi import APIRouter
from app.hotels.dao import HotelsDAO

router = APIRouter(
    prefix='/hotels',
    tags=['hotels | Отели']
)

@router.get('/list')
async def get_hotels(location: str, date_from: date, date_to: date):
    hotels_list_by_location = await HotelsDAO.rooms_left_by_hotel(location, date_from, date_to)
    return hotels_list_by_location


@router.get('/{hotel_id}/rooms')
async def get_rooms_by_hotel(hotel_id: int, date_from: date, date_to: date):
    rooms_by_hotel = await HotelsDAO.get_rooms_by_hotel(hotel_id, date_from, date_to)
    return rooms_by_hotel


@router.get('/features/{hotel_id}')
async def get_hotel_features(hotel_id: int):
    result = await HotelsDAO.get_hotel_features(hotel_id=hotel_id)
    if not result:
        raise HotelNotFound
    return result
