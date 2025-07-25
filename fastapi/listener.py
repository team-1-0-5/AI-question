from DAO.models import JoinSpeech
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Form
from fastapi.responses import JSONResponse
from typing import Dict, Set, List, Tuple
from DAO.models import User, Question, QuestionUser, Allocation, Speech, SpeechQuestion
from tortoise.exceptions import DoesNotExist
import json
from datetime import datetime
import asyncio

router = APIRouter(
    prefix="/listener",
    tags=["listener"],
    responses={404: {"description": "Not Found"}}
)

# 全局存储演讲推送信息 - 按用户存储
user_lecture_push_info: Dict[Tuple[int, int], Dict[int, List[int]]] = {}  # (uid, lid) -> {times: [qid1, qid2, ...]}
current_ppt_page: Dict[int, Tuple[int, int]] = {}  # lid -> (current_page, pic_fid)

# 题目推送和PPT推送的连接池 - 现在存储用户ID和WebSocket的映射
question_ws_pool: Dict[int, Dict[int, Set[WebSocket]]] = {}  # lid -> uid -> set of WebSocket
ppt_ws_pool: Dict[int, Set[WebSocket]] = {}  # lid -> set of WebSocket (PPT推送仍然是广播)


async def ws_connect(pool: Dict[int, Dict[int, Set[WebSocket]]], uid: int, lid: int, websocket: WebSocket):
    await websocket.accept()

    # 初始化数据结构
    if lid not in pool:
        pool[lid] = {}
    if uid not in pool[lid]:
        pool[lid][uid] = set()

    # 添加WebSocket到连接池
    pool[lid][uid].add(websocket)


def ws_disconnect(pool: Dict[int, Dict[int, Set[WebSocket]]], uid: int, lid: int, websocket: WebSocket):
    if lid in pool and uid in pool[lid] and websocket in pool[lid][uid]:
        pool[lid][uid].remove(websocket)
        if not pool[lid][uid]:
            del pool[lid][uid]
            if not pool[lid]:
                del pool[lid]


@router.websocket("/ws/question")
async def ws_question(websocket: WebSocket, uid: int, lid: int):
    await ws_connect(question_ws_pool, uid, lid, websocket)
    try:
        while True:
            # 保持连接，不处理接收的消息
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_disconnect(question_ws_pool, uid, lid, websocket)


@router.websocket("/ws/ppt")
async def ws_ppt(websocket: WebSocket, uid: int, lid: int):
    # PPT连接池保持原样，因为PPT推送是广播
    await websocket.accept()
    if lid not in ppt_ws_pool:
        ppt_ws_pool[lid] = set()
    ppt_ws_pool[lid].add(websocket)

    try:
        # 如果有当前PPT信息，立即发送给新连接的客户端
        if lid in current_ppt_page:
            page, pic_fid = current_ppt_page[lid]
            await websocket.send_text(json.dumps({
                "page": page,
                "pic_fid": pic_fid
            }))

        while True:
            # 保持连接，不处理接收的消息
            await websocket.receive_text()
    except WebSocketDisconnect:
        if lid in ppt_ws_pool and websocket in ppt_ws_pool[lid]:
            ppt_ws_pool[lid].remove(websocket)
            if not ppt_ws_pool[lid]:
                del ppt_ws_pool[lid]


# 推送函数（供演讲者端调用） - 精确推送给特定用户
async def push_questions(uid: int, lid: int, qids: List[int], times: int):
    # 存储推送信息 - 按用户和演讲ID存储
    key = (uid, lid)
    if key not in user_lecture_push_info:
        user_lecture_push_info[key] = {}
    user_lecture_push_info[key][times] = qids

    # 获取题目详情
    questions = []
    for qid in qids:
        try:
            question = await Question.get(question_id=qid)
            questions.append({
                "qid": qid,
                "question": question.question,
                "choices": question.options.split(";")
            })
        except DoesNotExist:
            continue

    print(question_ws_pool, lid in question_ws_pool, uid in question_ws_pool[lid])
    # 推送题目给特定用户
    if lid in question_ws_pool and uid in question_ws_pool[lid]:
        data = {"questions": questions, "times": times}
        print(data)
        # 发送给该用户的所有连接（可能多个标签页）
        for ws in list(question_ws_pool[lid][uid]):
            try:
                print(data)
                await ws.send_text(json.dumps(data))
            except Exception as e:
                # 处理发送失败的情况（如连接已关闭）
                print(f"Failed to send to user {uid}: {str(e)}")
                # 从连接池中移除无效连接
                if ws in question_ws_pool[lid][uid]:
                    question_ws_pool[lid][uid].remove(ws)


# 推送PPT页面 - 保持广播
async def push_ppt(lid: int, page: int, pic_fid: int):
    # 存储当前PPT页面
    current_ppt_page[lid] = (page, pic_fid)

    # 广播PPT更新
    if lid in ppt_ws_pool:
        data = {"page": page, "pic_fid": pic_fid}
        for ws in list(ppt_ws_pool[lid]):
            try:
                await ws.send_text(json.dumps(data))
            except:
                # 处理无效连接
                pass


@router.post("/post_answer")
async def post_answer(
        uid: int = Form(...),
        qids: List[int] = Form(...),
        answers: List[int] = Form(...)
):
    # 验证参数长度
    if len(qids) != len(answers):
        return JSONResponse({"error": "qids and answers length mismatch"}, status_code=400)

    # 查询正确答案
    correct = 0
    for idx, qid in enumerate(qids):
        try:
            question = await Question.get(question_id=qid)
            user_answer = str(answers[idx])
            # 记录或更新用户答案
            await QuestionUser.update_or_create(
                question_id=qid,
                user_id=uid,
                user_answer=user_answer
            )

            # 判断是否正确
            if user_answer == question.answer:
                correct += 1
        except DoesNotExist:
            # 题目不存在时跳过
            continue

    # 计算得分（避免除零错误）
    score = int(100 * correct / len(qids)) if qids else 0
    return JSONResponse({"score": score})


@router.post("/answer_res")
async def answer_res(
        uid: int = Form(...),
        lid: int = Form(...),
        times: int = Form(...)
):
    # 获取该次推送的题目ID - 按用户获取
    key = (uid, lid)
    try:
        qids = user_lecture_push_info[key][times]
    except KeyError:
        return JSONResponse({"error": "No questions found for this times"}, status_code=404)

    # 查询题目详情
    questions_list = []
    user_answers = []
    true_answers = []
    reason = []

    for qid in qids:
        try:
            question = await Question.get(question_id=qid)
            questions_list.append({
                "qid": qid,
                "question": question.question,
                "choices": question.options.split(";")
            })

            # 正确答案转换为整数
            true_answers.append(int(question.answer))

            # 获取用户答案
            try:
                user_answer = await QuestionUser.get(question_id=qid, user_id=uid)
                # 处理可能的空答案
                user_answers.append(int(user_answer.user_answer) if user_answer.user_answer else -1)
            except DoesNotExist:
                user_answers.append(-1)  # -1 表示未作答

            reason.append(question.analysis)
        except DoesNotExist:
            # 题目不存在时跳过
            continue

    return JSONResponse({
        "questions": questions_list,
        "user_answers": user_answers,
        "true_answers": true_answers,
        "reason": reason
    })


# 加入演讲接口
@router.post("/join")
async def join_lecture(uid: int = Form(...), lid: int = Form(...)):
    try:
        # 检查是否已加入
        exists = await JoinSpeech.exists(user_id=uid, speech_id=lid)
        if not exists:
            await JoinSpeech.create(user_id=uid, speech_id=lid)
        return {"res": True}
    except Exception as e:
        return {"res": False}


# 历史加入的演讲接口
@router.post("/history")
async def history(uid: int = Form(...)):
    from DAO.models import JoinSpeech, Speech, Create, User, SpeechFile
    # 1. 查找用户加入的所有演讲id
    joined = await JoinSpeech.filter(user_id=uid).all()
    speech_ids = [j.speech_id for j in joined]
    if not speech_ids:
        return {"data": []}
    # 2. 查找演讲详情
    speeches = await Speech.filter(speech_id__in=speech_ids).all()
    result = []
    for speech in speeches:
        # 获取演讲者用户名
        creator = await Create.filter(speech_id=speech.speech_id).first()
        speaker = ""
        if creator:
            user = await User.filter(user_id=creator.user_id).first()
            speaker = user.username if user else ""
        # 获取文件id列表
        files = await SpeechFile.filter(speech_id=speech.speech_id).all()
        fids = [f.file_id for f in files]
        result.append({
            "lid": speech.speech_id,
            "name": speech.title,
            "speaker": speaker,
            "start_time": str(speech.begin_time),
            "state": speech.state,
            "fids": fids
        })
    return {"data": result}