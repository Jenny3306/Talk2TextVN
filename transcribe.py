# transcribe.py
# Chức năng: dùng Whisper để chuyển audio thành text, log latency

import whisper
import time
import json
import os
from datetime import datetime
from config import WHISPER_MODEL, LANGUAGE, RESULTS_DIR

# Load model một lần duy nhất để tránh load lại mỗi lần gọi
_model = None

def get_model(model_name: str = WHISPER_MODEL):
    """
    Load Whisper model, cache lại để dùng nhiều lần.
    Lần đầu chạy sẽ tự download model (~75MB với tiny).
    """
    global _model
    if _model is None:
        print(f"Đang load Whisper model '{model_name}'...")
        print("(Lần đầu chạy sẽ tự download model, chờ chút...)")
        _model = whisper.load_model(model_name)
        print(f"Load model xong!")
    return _model


def transcribe(audio_input, model_name: str = WHISPER_MODEL) -> dict:
    """
    Chuyển audio thành text bằng Whisper.
    - audio_input: đường dẫn file .wav (str) hoặc numpy array float32
    - return: dict chứa text, latency, model, timestamp
    """
    model = get_model(model_name)

    print("Đang nhận dạng giọng nói...")
    start_time = time.time()

    result = model.transcribe(
        audio_input,
        language=LANGUAGE,
        verbose=False       # Tắt log chi tiết của Whisper
    )

    latency = round(time.time() - start_time, 3)
    raw_text = result["text"].strip()

    output = {
        "raw_text": raw_text,
        "latency_s": latency,
        "model": model_name,
        "language": LANGUAGE,
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S")
    }

    print(f"Nhận dạng xong! ({latency}s)")
    print(f"Raw text: {raw_text}")
    return output


def transcribe_and_save(audio_input, model_name: str = WHISPER_MODEL) -> dict:
    """
    Transcribe và lưu kết quả ra file JSON trong results/.
    """
    result = transcribe(audio_input, model_name)

    # Lưu kết quả
    os.makedirs(RESULTS_DIR, exist_ok=True)
    save_path = os.path.join(
        RESULTS_DIR,
        f"transcription_{result['timestamp']}.json"
    )
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Đã lưu kết quả: {save_path}")
    return result