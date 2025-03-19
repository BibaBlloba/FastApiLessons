from src.database import async_session_maker_null_pool
from src.schemas.hotels import HotelAdd
from utils.db_manager import DbManager


async def test_add_hotel():
    hotel_add = HotelAdd(title="Hotel 1", location="Hotel location")

    async with DbManager(session_factory=async_session_maker_null_pool) as db:
        new_hotel_data = await db.hotels.add(hotel_add)
        await db.commit()
