import shutil

# TODO: В идеале импортов fastapi не должно быть. В место них можно использовать интерфейс
from fastapi import BackgroundTasks, UploadFile
from services.base import BaseService
from tasks.tasks import resize_and_save_image


class ImageService(BaseService):
    def upload_image(self, file: UploadFile, background_tasks: BackgroundTasks):
        image_path = f'src/static/images/{file.filename}'
        with open(image_path, 'wb+') as new_file:
            shutil.copyfileobj(fsrc=file.file, fdst=new_file)

        # resize_and_save_image.delay(image_path, file.filename)

        background_tasks.add_task(resize_and_save_image, image_path, file.filename)
