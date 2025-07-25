import os
import time

import pythoncom
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist
import multiprocessing
import API.main as API

import speaker
import listener
import statistics
from DAO.models import User, File, UserFile, Speech, SpeechFile, JoinSpeech, Create
from config import DB_CONFIG

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)
# 数据库绑定
register_tortoise(
    app,
    config=DB_CONFIG,
    add_exception_handlers=True,
)

app.include_router(speaker.router)
app.include_router(statistics.router)
app.include_router(listener.router)


@app.get("/")
async def index():
    users = await User.all()
    return users


# 创建上传目录
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)



@app.post("/upload")
async def upload_file(
        file: UploadFile = File(),
        uid: int = Form(...),
        type: str = Form(...)
):
    # 验证文件类型
    allowed_types = ["courseware"]
    if type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")

    try:
        # 创建安全的文件名
        filename = f"{uid}_{time.time()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # 保存文件
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # 创建数据库记录
        file_record = await File.create(
            file_address=file_path,
            file_type=type
        )

        # 关联用户和文件
        await UserFile.create(
            user_id=uid,
            file_id=file_record.file_id
        )


        # PPT转文字（同步处理，用户需等待）
        if file_path.lower().endswith(('.ppt', '.pptx')):
            output_dir = os.path.splitext(file_path)[0] + "_text"
            print(file_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            text_list = API.ppt_to_text_list(file_path,False)
            txt_path = os.path.join(output_dir, "content.txt")
            with open(txt_path, "w", encoding="utf-8") as txtf:
                for i, page in enumerate(text_list, 1):
                    txtf.write(f"--- Page {i} ---\n{page}\n\n")


        return {"fid": file_record.file_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download")
async def download_file(
        fid: int = Form(...),  # 文件ID
        uid: int = Form(...)  # 用户ID
):
    try:
        # 1. 验证文件是否存在
        file_record = await File.get(file_id=fid)

        # # 2. 验证用户是否有权限访问该文件
        # # 检查user_file表中是否存在对应的用户-文件关系
        # exists = await UserFile.exists(user_id=uid, file_id=fid)
        #
        # if not exists:
        #     raise HTTPException(
        #         status_code=403,
        #         detail="You do not have permission to access this file"
        #     )

        # 3. 检查文件是否存在
        file_path = file_record.file_address
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail="File not found on server"
            )

        # 4. 返回文件
        # 自动设置Content-Type和Content-Disposition
        return FileResponse(
            file_path,
            filename=os.path.basename(file_path),
            media_type="application/octet-stream"
        )

    except DoesNotExist:
        # 处理文件不存在的情况
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    except Exception as e:
        # 其他错误处理
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/file_info")
async def get_combined_info(fid: int = Form(...), uid: int = Form(...)):
    file = await File.get_or_none(file_id=fid)
    user = await User.get_or_none(user_id=uid)
    # 文件名处理：取原始文件名
    file_name = None
    size = None
    if file:
        # 文件名为上传时的原始名（去除路径前缀）
        file_name = os.path.basename(file.file_address)
        # 获取本地文件大小
        if os.path.exists(file.file_address):
            size = os.path.getsize(file.file_address)
        else:
            size = 0
    return {
        "fid": fid,
        "file_name": file_name,
        "owner": user.username if user else None,
        "size": size
    }


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = await User.get_or_none(username=username)

    if not user or user.password != password:
        return {"res": False}

    # 将数字类型转换为中文描述
    user_type_str = "听众" if user.user_type == 0 else "演讲者"

    return {
        "res": True,
        "uid": user.user_id,
        "type": user_type_str
    }


# 注册接口
@app.post("/sign")
async def signup(username: str = Form(...), password: str = Form(...), user_type: str = Form(...)):
    # 验证用户类型输入
    if user_type not in ["听众", "演讲者"]:
        raise HTTPException(
            status_code=400,
            detail="用户类型必须是'听众'或'演讲者'"
        )

    # 检查用户名是否已存在
    exists = await User.exists(username=username)
    if exists:
        return {"res": False}

    # 转换用户类型为数字
    user_type_val = 0 if user_type == "听众" else 1

    # 创建新用户
    await User.create(
        username=username,
        password=password,
        user_type=user_type_val
    )

    return {"res": True}


@app.post("/lecture_detail")
async def get_lecture_detail(lid: int = Form(...)):
    speech = await Speech.filter(speech_id=lid).first()
    if not speech:
        raise HTTPException(
            status_code=404,
            detail="演讲未找到"
        )
    files = await SpeechFile.filter(speech_id=lid).all()
    fids = [file.file_id for file in files]
    join_num = await JoinSpeech.filter(speech_id=lid).count()
    user_id = await Create.filter(speech_id=lid).first()
    speech_creator = await User.filter(user_id=user_id.user_id).first()
    return {
        "lid": speech.speech_id,
        "name": speech.title,
        "speaker": speech_creator.username,
        "start_time": speech.begin_time,
        "fids": fids,
        "join_num": join_num
    }


@app.post("/all_lecture")
async def get_all_lecture(uid: int = Form(None)):
    speeches=[]
    if uid is not None:
        create_files = await Create.filter(user_id=uid).all()
        speech_ids = {cf.speech_id for cf in create_files}
        for id in speech_ids:
            speech=await Speech.filter(speech_id=id).first()
            speeches.append(speech)
    else:
        speeches = await Speech.all()
    results = []
    for speech in speeches:
        files = await SpeechFile.filter(speech_id=speech.speech_id).all()
        fids = [file.file_id for file in files]
        user_id = await Create.filter(speech_id=speech.speech_id).first()
        speech_creator = await User.filter(user_id=user_id.user_id).first()
        results.append({
            "lid": speech.speech_id,
            "name": speech.title,
            "speaker": speech_creator.username,
            "start_time": speech.begin_time,
            "state": speech.state,
            "fids": fids
        })

    return results


if __name__ == '__main__':
    uvicorn.run(app)
