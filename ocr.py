import io
import re
from PIL import Image, ImageEnhance, ImageOps

def extract_english(data: bytes) -> str:
    if not data:
        raise ValueError("图片为空")
    try:
        image = Image.open(io.BytesIO(data))
        image.load()
        image = ImageOps.exif_transpose(image).convert("L")
        image = ImageEnhance.Contrast(image).enhance(1.8)
        if image.width < 1200:
            scale = 1200 / image.width
            image = image.resize((1200, int(image.height * scale)))
    except Exception as e:
        raise ValueError("无法读取图片，请重新拍摄") from e
    try:
        import pytesseract
        text = pytesseract.image_to_string(image, lang="eng", config="--psm 6")
    except ImportError as e:
        raise RuntimeError("请先执行 pip install -r requirements.txt") from e
    except Exception as e:
        raise RuntimeError("OCR不可用：请安装Tesseract OCR并加入PATH") from e
    lines = []
    for line in text.splitlines():
        line = re.sub(r"[^A-Za-z0-9\s.,!?;:'\"()\-]", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        if re.search("[A-Za-z]", line):
            lines.append(line)
    if not lines:
        raise ValueError("未识别到英文，请在光线充足处重试")
    return "\n".join(lines)
