from app.dao.base import BaseDAO
from app.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Rooms
