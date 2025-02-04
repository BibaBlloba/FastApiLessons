from models.bookings import BookingsOrm
from repos.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Hotel
