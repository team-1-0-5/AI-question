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
        # 1. 查找该用户当天加入的所有演讲（start_time在当天）
        joined = await JoinSpeech.filter(user_id=uid)
        if not joined:
            rates.append(None)
            continue
        joined_speech_ids = [j.speech_id for j in joined]
        # 查找这些演讲的start_time在当天的
        speeches = await User.filter(user_id=uid)
        from DAO.models import Speech
        speeches_today = await Speech.filter(speech_id__in=joined_speech_ids, begin_time__gte=start, begin_time__lt=end)
        if not speeches_today:
            rates.append(None)
            continue
        speech_ids_today = [s.speech_id for s in speeches_today]
        # 2. 查找当天这些演讲的所有题目
        from DAO.models import SpeechQuestion
        speech_questions = await SpeechQuestion.filter(speech_id__in=speech_ids_today).all()
        question_ids = [sq.question_id for sq in speech_questions]
        if not question_ids:
            rates.append(None)
            continue
        # 3. 查找该用户当天这些题目的答题情况
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
        rate = round(correct / total * 100, 2) if total > 0 else 0.0
        rates.append(rate)
    return {"rates": rates, "date": dates}