from pptx import Presentation
from PIL import Image
import io
import easyocr
import numpy as np
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.shapes.picture import Picture
from typing import Any
# 新增导入
import whisper

# 初始化 EasyOCR
reader = easyocr.Reader(['ch_sim', 'en'])  # 支持中英文

# 新增：初始化 Whisper 模型（使用 base 模型，速度快，准确率较高）
whisper_model = whisper.load_model("base")

def ocr_image_with_easyocr(img):
    """对PIL图片对象进行OCR识别，返回识别到的文本字符串"""
    ocr_result = reader.readtext(np.array(img), detail=0)
    texts = [item[1] for item in ocr_result if isinstance(item, (list, tuple)) and len(item) > 1]
    return '\n'.join(texts) if texts else ''

# 新增：音频转文字函数
def audio_to_text(audio_path):
    """将音频文件转为文字，支持mp3/wav/m4a等格式"""
    result = whisper_model.transcribe(audio_path)
    return result.get('text', '')

def ppt_to_text_list(ppt_path):
    prs = Presentation(ppt_path)
    all_pages = []
    for slide in prs.slides:
        page_text = []
        for shape in slide.shapes:
            # 提取文本
            text = getattr(shape, "text", None)
            if text and text.strip():
                page_text.append(text)
            # 提取图片并OCR
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                if isinstance(shape, Picture):
                    image = shape.image
                    image_bytes = image.blob
                    image_stream = io.BytesIO(image_bytes)
                    img = Image.open(image_stream)
                    ocr_text = ocr_image_with_easyocr(img)
                    if ocr_text:
                        page_text.append(ocr_text)
        all_pages.append('\n'.join(page_text))
    return all_pages

# 用法示例
if __name__ == "__main__":
    ppt_path = r"E:\软件大发现\AI-question\BESTTTTT_AI_Q\test.pptx"
    result = ppt_to_text_list(ppt_path)
    for i, page in enumerate(result, 1):
        print(f"--- Page {i} ---")
        print(page)
        print()
    # 新增：音频转文字演示
    audio_path = r"E:\软件大发现\AI-question\BESTTTTT_AI_Q\test_audio.wav"  # 替换为你的音频文件路径
    audio_text = audio_to_text(audio_path)
    print("--- Audio to Text ---")  
    print(audio_text) 