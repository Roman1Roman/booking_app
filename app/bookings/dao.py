from datetime import date

from sqlalchemy.dialects.postgresql import JSONB

from app.db import async_session
from sqlalchemy import select, and_, or_, func, insert, delete, cast, String

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add_booking(cls, room_id: int, user_id: int, date_from: date, date_to: date):
        async with async_session() as session:
            booked_rooms = select(Bookings).where(
                and_(Bookings.room_id == room_id,
                     or_(
                         and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                         and_(Bookings.date_from <= date_from, Bookings.date_to > date_from),
                     )
                )
            ).cte("booked_rooms")

            get_rooms_left = select(Rooms.quantity - func.count(booked_rooms.c.room_id).label("rooms_left")
                                ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.id == room_id).group_by(Rooms.quantity, booked_rooms.c.room_id)

            rooms_left = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()

            else:
                return None

    @classmethod
    async def find_all_by_user(cls, user_id: int):
        async with async_session() as session:
            query = select(cls.model.__table__.columns, Rooms.image_id, Rooms.description, Rooms.name, cast(Rooms.services, JSONB)
                           ).where(cls.model.user_id == user_id) \
                            .join(Rooms, cls.model.room_id == Rooms.id) \
                            .group_by(cls.model.id, Rooms.image_id, Rooms.description, Rooms.name, cast(Rooms.services, JSONB)) \
                            #.order_by(cls.model.id)
            result = await session.execute(query)
            return result.fetchall()

    @classmethod
    async def find_one_by_user(cls, user_id: int, booking_id: int):
        async with async_session() as session:
            query = select(cls.model).where(and_(cls.model.user_id == user_id, cls.model.id == booking_id))
            result = await session.execute(query)
            if not result:
                return None
            return result.scalars().one_or_none()

    @classmethod
    async def delete_booking_by_user(cls, user_id: int, booking_id: int):
        async with async_session() as session:
            query = delete(cls.model).where(and_(cls.model.user_id == user_id, cls.model.id == booking_id))
            await session.execute(query)
            await session.commit()
            return True
