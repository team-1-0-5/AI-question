from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Body
from fastapi.responses import JSONResponse
from typing import Dict, Set, List, Tuple
from DAO.models import User, Question, QuestionUser, Allocation, Speech, SpeechQuestion
from tortoise.exceptions import DoesNotExist
import json
from datetime import datetime
import asyncio

router = APIRouter()

# 全局存储演讲推送信息
lecture_push_info: Dict[int, Dict[int, List[int]]] = {}  # lid -> {times: [qid1, qid2, ...]}
current_ppt_page: Dict[int, Tuple[int, int]] = {}  # lid -> (current_page, pic_fid)

# 题目推送和PPT推送的连接池
question_ws_pool: Dict[int, Set[WebSocket]] = {}  # lid -> set of WebSocket
ppt_ws_pool: Dict[int, Set[WebSocket]] = {}  # lid -> set of WebSocket


async def ws_connect(pool: Dict[int, Set[WebSocket]], lid: int, websocket: WebSocket):
    await websocket.accept()
    if lid not in pool:
        pool[lid] = set()
    pool[lid].add(websocket)


def ws_disconnect(pool: Dict[int, Set[WebSocket]], lid: int, websocket: WebSocket):
    if lid in pool and websocket in pool[lid]:
        pool[lid].remove(websocket)
        if not pool[lid]:
            del pool[lid]


@router.websocket("/ws/question")
async def ws_question(websocket: WebSocket, uid: int, lid: int):
    await ws_connect(question_ws_pool, lid, websocket)
    try:
        while True:
            # 保持连接，不处理接收的消息
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_disconnect(question_ws_pool, lid, websocket)


@router.websocket("/ws/ppt")
async def ws_ppt(websocket: WebSocket, uid: int, lid: int):
    await ws_connect(ppt_ws_pool, lid, websocket)
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
        ws_disconnect(ppt_ws_pool, lid, websocket)


# 推送函数（供演讲者端调用）
async def push_questions(lid: int, qids: List[int], times: int):
    # 存储推送信息
    if lid not in lecture_push_info:
        lecture_push_info[lid] = {}
    lecture_push_info[lid][times] = qids

    # 获取题目详情
    questions = []
    for qid in qids:
        try:
            question = await Question.get(question_id=qid)
            questions.append({
                "qid": qid,
                "question": question.question,
                "choices": question.options.split("|")
            })
        except DoesNotExist:
            continue

    # 推送题目
    if lid in question_ws_pool:
        data = {"questions": questions, "times": times}
        for ws in list(question_ws_pool[lid]):
            await ws.send_text(json.dumps(data))


# 推送PPT页面
async def push_ppt(lid: int, page: int, pic_fid: int):
    # 存储当前PPT页面
    current_ppt_page[lid] = (page, pic_fid)

    # 推送PPT
    if lid in ppt_ws_pool:
        data = {"page": page, "pic_fid": pic_fid}
        for ws in list(ppt_ws_pool[lid]):
            await ws.send_text(json.dumps(data))


@router.post("/post_answer")
async def post_answer(
        uid: int = Body(...),
        qids: List[int] = Body(...),
        answers: List[int] = Body(...)
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
                defaults={"user_answer": user_answer}
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
        uid: int = Body(...),
        lid: int = Body(...),
        times: int = Body(...)
):
    # 获取该次推送的题目ID
    try:
        qids = lecture_push_info[lid][times]
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
                "choices": question.options.split("|")
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

            reason.append(question.explanation if hasattr(question, 'explanation') else "暂无解析")
        except DoesNotExist:
            # 题目不存在时跳过
            continue

    return JSONResponse({
        "questions": questions_list,
        "user_answers": user_answers,
        "true_answers": true_answers,
        "reason": reason
    })