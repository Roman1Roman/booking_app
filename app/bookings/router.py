from datetime import date

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from app.exceptions import BookingNotFound, BookingNotAvailable
from app.bookings.dao import BookingDAO
from app.bookings.models import Bookings
from app.bookings.schemas import SBookingResponse, SBookingUserResponse
from app.users.models import Users
from app.users.dependencies import get_current_user


router = APIRouter(
    prefix='/bookings',
    tags=['bookings | Бронирования']
)


@router.get('/user_bookings')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingUserResponse]:
    result = await BookingDAO.find_all_by_user(user_id=user.id)
    if not result:
        raise BookingNotFound
    return result


@router.get('/{booking_id}')
async def get_booking_by_id(booking_id: int, user: Users = Depends(get_current_user)) -> SBookingResponse:
    result = await BookingDAO.find_one_by_user(user_id=user.id, booking_id=booking_id)
    if not result:
        raise BookingNotFound
    return result


@router.post('/add_booking')
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)) -> SBookingResponse:
    result = await BookingDAO.add_booking(user_id=user.id,
                                          room_id=room_id,
                                          date_from=date_from,
                                          date_to=date_to)
    if not result:
        raise BookingNotAvailable
    return result


@router.delete('/delete_booking/{booking_id}')
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    result = await BookingDAO.delete_booking_by_user(user_id=user.id, booking_id=booking_id)
    if not result:
        raise BookingNotFound


