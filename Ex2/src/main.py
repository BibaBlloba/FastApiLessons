import asyncio
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from time import sleep

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

from api.dependencies import get_db
from src.api.auth import router as router_auth
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.hotels import router as router_hotels
from src.api.images import router as router_images
from src.api.rooms import router as router_rooms
from src.init import redis_manager


async def get_bookings_today_checkin():
    async for db in get_db():
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


async def run_send_emails_regular():
    while True:
        await asyncio.sleep(5)
        await get_bookings_today_checkin()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте проекта
    asyncio.create_task(run_send_emails_regular())
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.client), prefix="fastapi-cache")
    yield
    await redis_manager.close()
    # При выключении/перезагрузки проекта


app = FastAPI(lifespan=lifespan)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_auth)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
