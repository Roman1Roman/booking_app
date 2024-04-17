from datetime import date

from sqlalchemy import select, func, and_, cast, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import or_
from sqlalchemy.sql.functions import coalesce

from app.db import async_session
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.hotels.schemas import SHotelResponse, SHotelsCustom
from app.rooms.models import Rooms
from app.bookings.models import Bookings


class HotelsDAO(BaseDAO):
    model = Hotels


    @classmethod
    async def find_by_location(cls, location: str) -> list[SHotelResponse]:
        async with async_session() as session:
            query = select(cls.model.__table__.columns).where(func.lower(cls.model.location).like(func.lower(f'%{location}%')))
            result = await session.execute(query)
            return result.mappings().all()


    @classmethod
    async def rooms_left_by_hotel(cls, location: str, date_from: date, date_to: date) -> list[SHotelsCustom]:
        async with async_session() as session:
            # Определение моделей таблиц для использования в запросе
            hotels = Hotels
            rooms = Rooms
            bookings = Bookings

            # Подзапрос для получения информации о номерах отеля
            hotels_rooms_subquery = (
                select(
                    hotels.location.label('location'),
                    hotels.id.label('hotel_id'),
                    hotels.name.label('name'),
                    cast(hotels.services, String).label('services'),
                    hotels.rooms_quantity.label('rooms_quantity'),
                    hotels.image_id.label('image_id'),
                    rooms.id.label('room_id')
                )
                .select_from(rooms).join(hotels, hotels.id == rooms.hotel_id)
                .where(func.lower(hotels.location).like(func.lower(f'%{location}%')))
                .alias('hotels_rooms')
            )

            # Основной запрос для подсчета количества бронирований
            bookings_counts_subquery = (
                select(
                    hotels_rooms_subquery.c.hotel_id,
                    func.count(bookings.room_id).label('bookings_count')
                )
                .select_from(hotels_rooms_subquery.join(
                    bookings,
                    and_(
                        bookings.room_id == hotels_rooms_subquery.c.room_id,
                        ~((bookings.date_from > date_to) | (bookings.date_to < date_from))
                    ),
                    isouter=True
                ))
                .group_by(hotels_rooms_subquery.c.hotel_id)
                .alias('bookings_counts')
            )

            # Основной запрос для получения свободных комнат
            query = (
                select(
                    hotels_rooms_subquery.c.location,
                    hotels_rooms_subquery.c.hotel_id,
                    hotels_rooms_subquery.c.name,
                    cast(hotels_rooms_subquery.c.services, JSONB).label('services'),
                    hotels_rooms_subquery.c.rooms_quantity,
                    hotels_rooms_subquery.c.image_id,
                    func.coalesce(
                        hotels_rooms_subquery.c.rooms_quantity - bookings_counts_subquery.c.bookings_count,
                        hotels_rooms_subquery.c.rooms_quantity
                    ).label('rooms_left')
                )
                .select_from(hotels_rooms_subquery.join(
                    bookings_counts_subquery,
                    hotels_rooms_subquery.c.hotel_id == bookings_counts_subquery.c.hotel_id
                )).distinct()
            )

            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def get_rooms_by_hotel(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session() as session:

            booked_rooms = select(Bookings.room_id, func.count(Bookings.room_id).label('rooms_booked')).where(
                or_(
                    and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                    and_(Bookings.date_from <= date_from, Bookings.date_to > date_from),
                )) \
                .select_from(Bookings).group_by(Bookings.room_id).cte("booked_rooms")

            get_rooms = select(Rooms.__table__.columns, (Rooms.quantity - coalesce(booked_rooms.c.rooms_booked, 0)).label('rooms_left'),
                               (Rooms.price*(date_to - date_from).days).label('total_cost')). \
            select_from(Rooms).join(booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True). \
            where(Rooms.hotel_id == hotel_id).order_by(Rooms.id)

            result = await session.execute(get_rooms)
            return result.mappings().all()


    @classmethod
    async def get_hotel_features(cls, hotel_id: int):
        async with async_session() as session:
            query = select(cls.model.__table__.columns).where(cls.model.id == hotel_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()