from src.models.bookings import BookingsOrm
from repos.base import BaseRepository
from schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking
