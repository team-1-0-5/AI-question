from datetime import datetime
from typing import List

from fastapi import Form, APIRouter

from DAO.models import Speech

router = APIRouter(
    prefix="/speaker",
    tags=["speaker"],
    responses={404: {"description": "Not Found"}}
)


@router.post("/lecture_create")
async def create_speech(name: str = Form(...), uid: int = Form(), describe: str = Form(...),
                        file_ids: List[int] = Form(...), start_time: datetime = Form(...)):

    speech = await Speech.create(title=name, description=describe, begin_time=start_time)

    print(file_ids)
    return speech.speech_id
