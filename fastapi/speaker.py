import os
from datetime import datetime
from typing import List
import API.main as API
from fastapi import Form, APIRouter, HTTPException
from tortoise.exceptions import DoesNotExist

from DAO.models import Speech, Create, SpeechFile, File, Question, JoinSpeech
from listener import push_ppt, push_questions

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
    speech = await Speech.create(title=name, description=describe, begin_time=start_time, state="upcoming")
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


@router.post("/post_answer")
async def post_answer(lid: int = Form(...), fid: int = Form(None), start_page: int = Form(None),
                      end_page: int = Form(None)):

    files_path = []
    if fid is not None:
        file = await File.filter(file_id=fid).first()
        files_path.append(file.file_address)
    else:
        file_ids = await SpeechFile.filter(speech_id=lid).all()
        for id in file_ids:
            file2 = await File.filter(file_id=id.file_id).first()
            file_path2 = file2.file_address
            files_path.append(file_path2)

    base_dir = os.path.dirname(os.path.abspath(__file__))

    text_list = []
    for file_path in files_path:
        full_path = os.path.join(base_dir, file_path)
        if not os.path.exists(full_path):
            print("文件不存在")
        text_list += API.ppt_to_text_list(full_path)

    if start_page is None:
        start_page = 1
    if end_page is None:
        end_page = len(text_list)
    listener_ids = await JoinSpeech.filter(speech_id=lid).all()

    for listener_id in listener_ids:
        result = API.summarize_and_generate_questions(text_list[start_page:end_page],
                                                      "a9205aba794f4f00acf33541eddbcd17.vqgIdbW54DlezvJh")
        try:
            # 解析问题列表
            questions = [q.strip() for q in result['questions_str'].split('\n') if q.strip()]

            # 解析选项（每组4个选项）
            all_options = [opt.strip() for opt in result['options_str'].split('\n') if opt.strip()]
            option_groups = [all_options[i:i + 4] for i in range(0, len(all_options), 4)]

            # 解析答案索引
            answer_indices = [int(idx.strip()) for idx in result['answer_indices_str'].split('\n') if idx.strip()]

            # 解析解析文本
            explanations = [exp.strip() for exp in result['explanations_str'].split('\n') if exp.strip()]

            # 验证数据一致性
            if len(questions) != len(option_groups) or len(questions) != len(answer_indices) or len(questions) != len(
                    explanations):
                raise HTTPException(
                    status_code=400,
                    detail=f"数据长度不一致: 问题({len(questions)}), 选项组({len(option_groups)}), 答案({len(answer_indices)}), 解析({len(explanations)})"
                )
            q_ids=[]
            for i in range(len(questions)):
                # 获取正确答案文本
                correct_answer = option_groups[i][answer_indices[i]]

                # 创建并保存问题记录
                new_question=await Question.create(
                    question=questions[i],
                    options=";".join(option_groups[i]),  # 选项用分号分隔
                    answer=correct_answer,
                    analysis=explanations[i]
                )
                new_question_id=new_question.question_id
                q_ids.append(new_question_id)
            await push_questions(listener_id, lid, q_ids)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"处理错误: {str(e)}")
    return {'res':1}


# 添加演讲文件接口
@router.post("/add_file")
async def add_file(lid: int = Form(...), fid: int = Form(...)):
    try:
        # 检查演讲和文件是否存在
        speech = await Speech.get_or_none(speech_id=lid)
        file = await File.get_or_none(file_id=fid)
        if not speech or not file:
            return {"res": False}
        # 检查是否已关联，避免重复
        exists = await SpeechFile.exists(speech_id=lid, file_id=fid)
        if not exists:
            await SpeechFile.create(speech_id=lid, file_id=fid)
        return {"res": True}
    except Exception as e:
        print(f"添加演讲文件失败: {e}")
        return {"res": False}


@router.post("/show_ppt")
async def show_ppt(lid: int = Form(...), fid: int = Form(...), page: int = Form(...)):
    """
    展示PPT指定页，自动生成图片（如已生成则复用），并推送给听众
    """

    # 获取当前项目根目录
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. 查找文件路径
    file_obj = await File.get_or_none(file_id=fid)
    if not file_obj or not file_obj.file_address.lower().endswith(('.ppt', '.pptx')):
        return {"res": False, "msg": "文件不存在或不是PPT"}

    ppt_path = os.path.join(base_dir, file_obj.file_address)
    if not os.path.exists(ppt_path):
        return {"res": False, "msg": "PPT文件不存在"}

    # 2. 生成图片输出目录
    output_dir = os.path.splitext(ppt_path)[0] + "_imgs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 3. 检查图片是否已生成
    img_path = os.path.join(output_dir, f"{page}.JPG")
    if not os.path.exists(img_path):
        # 用office自动化生成所有图片（只生成一次）
        API.ppt_to_images_with_office(ppt_path, output_dir)
        # 检查目标图片是否生成
        if not os.path.exists(img_path):
            return {"res": False, "msg": "图片生成失败"}

    # 4. 将图片保存到File表（如已存在则复用）
    # 检查是否已有该图片文件
    rel_img_path = os.path.relpath(img_path, base_dir)
    file_rec = await File.get_or_none(file_address=rel_img_path)
    if not file_rec:
        file_rec = await File.create(file_address=rel_img_path, file_type="ppt_img")
    pic_fid = file_rec.file_id

    # 5. 统计总页数
    page_num = len([f for f in os.listdir(output_dir) if f.lower().endswith('.jpg')])

    # 6. 推送PPT页码和图片fid给所有听众
    await push_ppt(lid, page, pic_fid)

    return {"res": True, "page_num": page_num, "pic_fid": pic_fid}
