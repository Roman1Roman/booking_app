from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Hotels(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]
