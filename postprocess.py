# postprocess.py
# Chức năng: chuẩn hóa text sau khi Whisper nhận dạng

import re
import os
import json
import requests
from dotenv import load_dotenv
from config import ENABLE_PUNCTUATION, ENABLE_LINE_BREAKS, ENABLE_FILLER_REMOVAL

load_dotenv()

# ── Danh sách filler words tiếng Việt thường gặp ──────────────────────────
FILLER_WORDS = [
    r"\bừm+\b", r"\bừ+\b", r"\bờm+\b", r"\bờ+\b",
    r"\bà+\b",  r"\bạ+\b", r"\bthì\b", r"\bmà\b",
    r"\bnhỉ\b", r"\bnhé\b", r"\bnha\b", r"\bhe\b",
    r"\bkiểu\b",r"\bểu\b",  r"\bý\b", r"\bmn\b",
]

# ── Các cặp từ hay bị Whisper nhận dạng sai ───────────────────────────────
COMMON_CORRECTIONS = {
    "ko ": "không ",
    "k ":  "không ",
    "dc ": "được ",
    "đc ": "được ",
    "vs ":  "với ",
    "mk ": "mình ",
    "mn ": "mọi người ",
}

def remove_fillers(text: str) -> str:
    """Xóa filler words khỏi text."""
    for pattern in FILLER_WORDS:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    # Dọn khoảng trắng thừa sau khi xóa
    text = re.sub(r" {2,}", " ", text).strip()
    return text


def apply_corrections(text: str) -> str:
    """Sửa các từ viết tắt hoặc nhận dạng sai phổ biến."""
    for wrong, correct in COMMON_CORRECTIONS.items():
        text = text.replace(wrong, correct)
    return text


def capitalize_sentences(text: str) -> str:
    """Viết hoa chữ đầu mỗi câu."""
    if not text:
        return text
    # Viết hoa sau dấu . ! ?
    sentences = re.split(r"([.!?]+\s+)", text)
    result = ""
    for part in sentences:
        if part and not re.match(r"[.!?]+\s+", part):
            part = part[0].upper() + part[1:] if len(part) > 1 else part.upper()
        result += part
    # Viết hoa chữ đầu tiên
    if result:
        result = result[0].upper() + result[1:]
    return result


def add_punctuation(text: str) -> str:
    """
    Thêm dấu chấm cuối câu nếu chưa có.
    Rule đơn giản: nếu text không kết thúc bằng dấu câu thì thêm dấu chấm.
    """
    text = text.strip()
    if text and text[-1] not in ".!?,;:":
        text += "."
    return text


def add_line_breaks(text: str) -> str:
    """
    Thêm xuống dòng sau mỗi câu để dễ đọc hơn.
    """
    text = re.sub(r"([.!?])\s+", r"\1\n", text)
    return text.strip()


def normalize_with_rules(raw_text: str) -> str:
    """
    Pipeline rule-based đầy đủ.
    Chạy theo thứ tự: corrections → fillers → capitalize → punctuation → line breaks
    """
    text = raw_text

    text = apply_corrections(text)

    if ENABLE_FILLER_REMOVAL:
        text = remove_fillers(text)

    text = capitalize_sentences(text)

    if ENABLE_PUNCTUATION:
        text = add_punctuation(text)

    if ENABLE_LINE_BREAKS:
        text = add_line_breaks(text)

    return text

def normalize_with_gemma(raw_text: str) -> str:
    try:
        import google.genai as genai

        api_key = os.getenv("GEMMA_API_KEY")
        if not api_key:
            raise ValueError("Không tìm thấy GEMMA_API_KEY trong file .env")

        client = genai.Client(api_key=api_key)

        prompt = f"""Bạn là công cụ chuẩn hóa văn bản tiếng Việt.
Hãy chuẩn hóa đoạn text sau theo các quy tắc:
1. Thêm dấu câu phù hợp (. , ! ?)
2. Viết hoa đầu câu và tên riêng
3. Xóa filler words (ừm, à, ờ, thì, nha, nhé...)
4. Sửa từ viết tắt (ko→không, dc→được, mn→mọi người...)
5. Giữ nguyên nội dung, chỉ chỉnh format và chính tả

Text cần chuẩn hóa: {raw_text}

Chỉ trả về text đã chuẩn hóa, không giải thích, không thêm gì khác."""

        response = client.models.generate_content(
            model="gemma-3n-e4b-it",
            contents=prompt
        )
        result = response.text.strip()
        # Giới hạn output không quá 3x độ dài input
        max_len = max(len(raw_text) * 3, 100)
        return result[:max_len]

    except Exception as e:
        print(f"Gemma API lỗi: {e}")
        print("Fallback về rule-based...")
        return normalize_with_rules(raw_text)


def normalize_with_gemma_local(raw_text: str) -> str:
    """
    Dùng Gemma 3n chạy on-device qua Ollama — hoàn toàn offline.
    Không cần internet, không cần API key.
    """
    try:
        import ollama

        prompt = f"""Bạn là công cụ chuẩn hóa văn bản tiếng Việt.
Hãy chuẩn hóa đoạn text sau theo các quy tắc:
1. Thêm dấu câu phù hợp (. , ! ?)
2. Viết hoa đầu câu và tên riêng
3. Xóa filler words (ừm, à, ờ, thì, nha, nhé...)
4. Sửa từ viết tắt (ko→không, dc→được, mn→mọi người...)
5. Giữ nguyên nội dung, chỉ chỉnh format và chính tả

Text cần chuẩn hóa: {raw_text}

Chỉ trả về text đã chuẩn hóa, không giải thích, không thêm gì khác."""

        response = ollama.chat(
            model="gemma3n",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response["message"]["content"].strip()
        # Giới hạn output không quá 3x độ dài input
        max_len = max(len(raw_text) * 3, 100)
        return result[:max_len]

    except Exception as e:
        print(f"Gemma local lỗi: {e}")
        print("Fallback về rule-based...")
        return normalize_with_rules(raw_text)
    
def postprocess(raw_text: str, use_gemma: bool = False, use_local: bool = False) -> dict:
    """
    - use_gemma=True  : dùng Gemma qua API (cần internet)
    - use_local=True  : dùng Gemma on-device qua Ollama (offline)
    - mặc định        : rule-based
    """
    if use_local:
        cleaned_text = normalize_with_gemma_local(raw_text)
        method = "gemma-local"
    elif use_gemma:
        cleaned_text = normalize_with_gemma(raw_text)
        method = "gemma-api"
    else:
        cleaned_text = normalize_with_rules(raw_text)
        method = "rule-based"

    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "method": method
    }