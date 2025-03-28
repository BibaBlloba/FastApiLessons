from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class RoomsOrm(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    title: Mapped[str]
    desription: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    facilities: Mapped[list['FacilitiesOrm']] = relationship(
        back_populates='rooms',  # атрибут таблици, к которой нужно привязаться
        secondary='rooms_facilities',  # M2M таблица, через которую нужно связаться с другой моделью
    )
