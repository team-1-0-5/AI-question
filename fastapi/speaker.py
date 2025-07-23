from datetime import datetime
from typing import List

from fastapi import Form, APIRouter

from DAO.models import Speech, Create, SpeechFile

router = APIRouter(
    prefix="/speaker",
    tags=["speaker"],
    responses={404: {"description": "Not Found"}}
)


@router.post("/lecture_create")
async def create_speech(name: str = Form(...), uid: int = Form(...), describe: str = Form(None),
                        file_ids: List[int] = Form([]), start_time: datetime = Form(None)):
    if start_time is None:
        start_time = datetime.now()
    speech = await Speech.create(title=name, description=describe, begin_time=start_time,)
    await Create.create(user_id=uid, speech_id=speech.speech_id)
    for file_id in file_ids:
        await SpeechFile.create(speech_id=speech.speech_id, file_id=file_id)
    print(file_ids)
    return {"lids": speech.speech_id}
