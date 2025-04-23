import shutil

from fastapi import APIRouter, UploadFile
from fastapi.background import BackgroundTasks

from services.images import ImageService
from tasks.tasks import resize_and_save_image


router = APIRouter(prefix='/images', tags=['Изображения'])


@router.get('')
async def get_images():
    return {'status': 'ok'}


@router.post('')
async def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    ImageService().upload_image(file, background_tasks)
