import asyncio
import os
from time import sleep

from PIL import Image

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DbManager


@celery_instance.task
def test_task():
    sleep(5)
    print('Найс')


# @celery_instance.task
def resize_and_save_image(image_path, filename):
    # Открытие исходного изображения
    with Image.open(image_path) as img:
        # Список целевых ширин
        output_dir = 'src/static/images'
        target_widths = [1000, 500, 300]

        # Получаем исходную высоту и ширину
        original_width, original_height = img.size

        # Для каждой целевой ширины
        for width in target_widths:
            # Расчёт нового соотношения сторон
            aspect_ratio = original_height / original_width
            new_height = int(width * aspect_ratio)

            # Изменяем размер изображения
            resized_img = img.resize((width, new_height))

            # Формируем путь для сохранения
            output_path = os.path.join(output_dir, f'{width}_{filename}')

            # Сохраняем изображение
            resized_img.save(output_path)
            print(f'Изображение сохранено: {output_path}')


async def send_emails_to_users_with_today_checkin_helper():
    print(f'Функция {__name__} началасб')
    async with DbManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(bookings)


@celery_instance.task(name='booking_today_checkin')
def send_emails_to_users_with_today_checkin():
    asyncio.run(send_emails_to_users_with_today_checkin_helper())
