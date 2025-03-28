import shutil

from fastapi import APIRouter, UploadFile
from fastapi.background import BackgroundTasks


router = APIRouter(prefix="/images", tags=["Изображения"])


@router.get("")
async def get_images():
    return {"status": "ok"}


@router.post("")
async def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(fsrc=file.file, fdst=new_file)

    # resize_and_save_image.delay(image_path, file.filename)

    # background_tasks.add_task(resize_and_save_image, image_path, file.filename)
