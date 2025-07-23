from datetime import datetime, timedelta
from fastapi import APIRouter, Form
from tortoise.expressions import Q
from DAO.models import User, QuestionUser, Question, JoinSpeech, Allocation


router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
    responses={404: {"description": "Not Found"}}
)

@router.post("/personal_history_rate")
async def personal_history_rate(uid: int = Form(...), day: int = Form(...)):
    today = datetime.now().date()
    rates = []
    dates = []
    for i in range(day-1, -1, -1):
        d = today - timedelta(days=i)
        dates.append(d.strftime("%Y-%m-%d"))
        start = datetime.combine(d, datetime.min.time())
        end = start + timedelta(days=1)
        # 1. 查找该用户当天加入的所有演讲
        joined = await JoinSpeech.filter(user_id=uid)
        if not joined:
            rates.append(None)
            continue
        joined_speech_ids = [j.speech_id for j in joined]
        # 2. 查找当天分配给该用户的题目（allocation表，按times范围和speech_id）
        allocations = await Allocation.filter(user_id=uid, times__gte=start, times__lt=end)
        if not allocations:
            rates.append(None)
            continue
        question_ids = [a.question_id for a in allocations]
        if not question_ids:
            rates.append(None)
            continue
        # 3. 查找答题表（question_user）
        answers = await QuestionUser.filter(user_id=uid, question_id__in=question_ids)
        answer_map = {a.question_id: a.user_answer for a in answers}
        # 4. 查找题库表，统计正确率
        total = len(question_ids)
        correct = 0
        for qid in question_ids:
            q = await Question.get_or_none(question_id=qid)
            if not q:
                continue
            user_ans = answer_map.get(qid, None)
            if user_ans is not None and user_ans == q.answer:
                correct += 1
            # 未作答或作答错误都不加分
        rate = round(correct / total * 100, 2) if total > 0 else 0.0
        rates.append(rate)
    return {"rates": rates, "date": dates}