from pptx import Presentation
from PIL import Image
import io
import easyocr
import numpy as np
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.shapes.picture import Picture
from typing import Any

# 初始化 EasyOCR
reader = easyocr.Reader(['ch_sim', 'en'])  # 支持中英文

def ocr_image_with_easyocr(img):
    """对PIL图片对象进行OCR识别，返回识别到的文本字符串"""
    ocr_result = reader.readtext(np.array(img), detail=0)
    texts = [item[1] for item in ocr_result if isinstance(item, (list, tuple)) and len(item) > 1]
    return '\n'.join(texts) if texts else ''

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