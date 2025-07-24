import datetime

import pytest
import json
from fastapi.testclient import TestClient
from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.test import finalizer, initializer
from DAO.models import User, Question, QuestionUser, Speech, SpeechQuestion
from listener import router, push_questions, push_ppt, lecture_push_info, current_ppt_page

app = FastAPI()
app.include_router(router)

# 数据库配置
DB_URL = "sqlite://:memory:"


# 初始化测试数据库
@pytest.fixture(scope="module", autouse=True)
def initialize_tests(request):
    initializer(["DAO.models"], db_url=DB_URL, app_label="models")
    request.addfinalizer(finalizer)


@pytest.fixture
async def test_data():
    # 创建测试用户
    speaker = await User.create(
        username="test_speaker",
        password="password",
        user_type=1
    )

    listener = await User.create(
        username="test_listener",
        password="password",
        user_type=0
    )

    # 创建测试演讲
    speech = await Speech.create(
        title="Test Speech",
        description="Test Description",
        begin_time=datetime.now()
    )

    # 创建测试题目
    q1 = await Question.create(
        question="What is 2+2?",
        options="3|4|5|6",
        answer="1"  # 对应选项1（索引0）
    )

    q2 = await Question.create(
        question="Capital of France?",
        options="London|Paris|Berlin|Madrid",
        answer="1"  # 对应选项1（索引1）
    )

    # 关联演讲和题目
    await SpeechQuestion.create(speech_id=speech.speech_id, question_id=q1.question_id)
    await SpeechQuestion.create(speech_id=speech.speech_id, question_id=q2.question_id)

    return {
        "speaker_id": speaker.user_id,
        "listener_id": listener.user_id,
        "speech_id": speech.speech_id,
        "q1_id": q1.question_id,
        "q2_id": q2.question_id
    }


@pytest.mark.asyncio
async def test_websocket_connections(test_data):
    client = TestClient(app)

    # 测试题目WebSocket连接
    with client.websocket_connect(f"/ws/question?uid={test_data['listener_id']}&lid={test_data['speech_id']}") as ws:
        response = ws.receive_text()
        assert response is not None

    # 测试PPT WebSocket连接
    with client.websocket_connect(f"/ws/ppt?uid={test_data['listener_id']}&lid={test_data['speech_id']}") as ws:
        response = ws.receive_text()
        assert response is not None


@pytest.mark.asyncio
async def test_question_push(test_data):
    # 模拟题目推送
    await push_questions(
        test_data["speech_id"],
        [test_data["q1_id"], test_data["q2_id"]],
        1
    )

    # 验证推送信息已存储
    assert test_data["speech_id"] in lecture_push_info
    assert 1 in lecture_push_info[test_data["speech_id"]]
    assert len(lecture_push_info[test_data["speech_id"]][1]) == 2


@pytest.mark.asyncio
async def test_ppt_push(test_data):
    # 模拟PPT推送
    await push_ppt(test_data["speech_id"], 5, 202)

    # 验证PPT信息已存储
    assert test_data["speech_id"] in current_ppt_page
    assert current_ppt_page[test_data["speech_id"]] == (5, 202)


@pytest.mark.asyncio
async def test_post_answer(test_data):
    client = TestClient(app)

    # 提交答案
    response = client.post(
        "/post_answer",
        json={
            "uid": test_data["listener_id"],
            "qids": [test_data["q1_id"], test_data["q2_id"]],
            "answers": [1, 1]  # 答对第一题，答错第二题
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert data["score"] == 50  # 答对1题，共2题，得分50

    # 验证答案已存储
    user_answer = await QuestionUser.get(
        question_id=test_data["q1_id"],
        user_id=test_data["listener_id"]
    )
    assert user_answer.user_answer == "1"


@pytest.mark.asyncio
async def test_answer_res(test_data):
    client = TestClient(app)

    # 先模拟题目推送
    await push_questions(
        test_data["speech_id"],
        [test_data["q1_id"], test_data["q2_id"]],
        1
    )

    # 提交答案
    await QuestionUser.create(
        question_id=test_data["q1_id"],
        user_id=test_data["listener_id"],
        user_answer="1"  # 正确答案
    )

    await QuestionUser.create(
        question_id=test_data["q2_id"],
        user_id=test_data["listener_id"],
        user_answer="0"  # 错误答案
    )

    # 获取作答情况
    response = client.post(
        "/answer_res",
        json={
            "uid": test_data["listener_id"],
            "lid": test_data["speech_id"],
            "times": 1
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert len(data["questions"]) == 2
    assert "user_answers" in data
    assert data["user_answers"] == [1, 0]  # 用户的答案
    assert "true_answers" in data
    assert data["true_answers"] == [1, 1]  # 正确答案（都选索引1）
    assert "reason" in data
    assert len(data["reason"]) == 2


@pytest.mark.asyncio
async def test_invalid_post_answer(test_data):
    client = TestClient(app)

    # 测试长度不匹配
    response = client.post(
        "/post_answer",
        json={
            "uid": test_data["listener_id"],
            "qids": [test_data["q1_id"]],
            "answers": [1, 2]  # 长度不匹配
        }
    )
    assert response.status_code == 400

    # 测试无效题目ID
    response = client.post(
        "/post_answer",
        json={
            "uid": test_data["listener_id"],
            "qids": [999],  # 不存在的题目ID
            "answers": [1]
        }
    )
    assert response.status_code == 200  # 应该成功处理，只是跳过无效题目
    assert response.json()["score"] == 0


@pytest.mark.asyncio
async def test_invalid_answer_res(test_data):
    client = TestClient(app)

    # 测试无效演讲ID
    response = client.post(
        "/answer_res",
        json={
            "uid": test_data["listener_id"],
            "lid": 999,  # 不存在的演讲ID
            "times": 1
        }
    )
    assert response.status_code == 404

    # 测试无效波次
    response = client.post(
        "/answer_res",
        json={
            "uid": test_data["listener_id"],
            "lid": test_data["speech_id"],
            "times": 999  # 不存在的波次
        }
    )
    assert response.status_code == 404
