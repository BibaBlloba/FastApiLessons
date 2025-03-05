from celery import Celery

from src.config import settings

celery_instance = Celery(
    "tasks",  # Рандомное название
    broker=settings.redis_url,
    include=[
        "src.tasks.tasks",
    ],
)
