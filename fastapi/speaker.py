from datetime import datetime
from typing import List

from fastapi import Form, APIRouter, HTTPException
from tortoise.exceptions import DoesNotExist

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
    speech = await Speech.create(title=name, description=describe, begin_time=start_time, )
    await Create.create(user_id=uid, speech_id=speech.speech_id)
    for file_id in file_ids:
        await SpeechFile.create(speech_id=speech.speech_id, file_id=file_id)
    print(file_ids)
    return {"lids": speech.speech_id}


@router.post("/start_lecture")
async def start_lecture(lid: int = Form(...)):
    try:
        speech = await Speech.get(speech_id=lid)
        speech.state = "ongoing"
        await speech.save()

        return {"res": "演讲已开始"}

    except DoesNotExist:
        # 演讲不存在的情况
        raise HTTPException(
            status_code=404,
            detail=f"演讲ID {lid} 不存在"
        )
    except Exception as e:
        # 其他异常处理
        raise HTTPException(
            status_code=500,
            detail=f"更新状态失败: {str(e)}"
        )

@router.post("/end_lecture")
async def start_lecture(lid: int = Form(...)):
    try:
        speech = await Speech.get(speech_id=lid)
        speech.state = "ended"
        await speech.save()

        return {"res": "演讲已结束"}

    except DoesNotExist:
        # 演讲不存在的情况
        raise HTTPException(
            status_code=404,
            detail=f"演讲ID {lid} 不存在"
        )
    except Exception as e:
        # 其他异常处理
        raise HTTPException(
            status_code=500,
            detail=f"更新状态失败: {str(e)}"
        )
