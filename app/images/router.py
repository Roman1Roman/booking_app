from fastapi import UploadFile, APIRouter
import shutil

router = APIRouter(
    prefix='/images',
    tags=['images | download images']
)

@router.post('/upload')
async def add_hotel_image(file: UploadFile, name_id: int):
    with open(f"app/static/images/{name_id}.webp", "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)