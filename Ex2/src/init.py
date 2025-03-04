from src.config import settings
from src.connectors.resis_connector import RedisManager

redis_manager = RedisManager(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)
