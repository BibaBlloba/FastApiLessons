from datetime import date

from sqlalchemy import func, select

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


def rooms_ids_for_booking(
    hotel_id,
    date_from: date,
    date_to: date,
):
    rooms_count = (
        select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsOrm)
        .filter(
            BookingsOrm.date_from <= date_to,
            BookingsOrm.date_to >= date_from,
        )
        .group_by(BookingsOrm.room_id)
        .cte(name="rooms_booked")
    )
    rooms_left_table = (
        select(
            RoomsOrm.id.label("room_id"),
            (RoomsOrm.quanity - func.coalesce(rooms_count.c.rooms_booked, 0)).label(
                "rooms_left"
            ),
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
        .cte(name="rooms_left_table")
    )
    rooms_ids_for_hotel = select(RoomsOrm.id).filter_by(hotel_id=hotel_id).subquery()
    rooms_ids_to_get = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(
            rooms_left_table.c.rooms_left > 0,
            rooms_left_table.c.room_id.in_(select(rooms_ids_for_hotel)),
        )
    )

    return rooms_ids_to_get
