from src.schemas.hotels import HotelAdd


async def test_add_hotel(db):
    hotel_add = HotelAdd(title='Hotel 1', location='Hotel location')

    await db.hotels.add(hotel_add)
    await db.commit()
