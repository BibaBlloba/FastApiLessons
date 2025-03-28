import typing

if typing.TYPE_CHECKING:
    from src.models import RoomsOrm

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.rooms import RoomsOrm


class FacilitiesOrm(Base):
    __tablename__ = 'facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))

    rooms: Mapped[list['RoomsOrm']] = relationship(
        back_populates='facilities', secondary='rooms_facilities'
    )


# M2M
class RoomsFacilitiesOrm(Base):
    __tablename__ = 'rooms_facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey(RoomsOrm.id))
    facility_id: Mapped[int] = mapped_column(ForeignKey('facilities.id'))
