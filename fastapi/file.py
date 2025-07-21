import os
import time

import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi_cli import logging
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

import speaker
from DAO.models import User, File, UserFile
from config import DB_CONFIG

app = FastAPI()

#数据库绑定
register_tortoise(
    app,
    config=DB_CONFIG,
    add_exception_handlers=True,
)

app.include_router(speaker.router)


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

        filename = f"{uid}__{time.time()}_{file.filename}"
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

        # 2. 验证用户是否有权限访问该文件
        # 检查user_file表中是否存在对应的用户-文件关系
        exists = await UserFile.exists(user_id=uid, file_id=fid)

        if not exists:
            # 这里可以添加额外的公开文件检查逻辑（如果文件有公开属性）
            # 但根据当前数据库结构，我们只检查用户-文件关系
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this file"
            )

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
    return {
        "fid": fid,
        "file_name": file.file_address if file else None,
        "owner": user.username if user else None
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


if __name__ == '__main__':
    uvicorn.run(app)
