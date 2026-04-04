# audio_io.py
# Chức năng: ghi âm từ microphone, load và save file audio

import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import os
from datetime import datetime
from config import SAMPLE_RATE, CHANNELS, RECORD_SECONDS

def record_audio(duration: int = RECORD_SECONDS, save_path: str = None) -> str:
    """
    Ghi âm từ microphone.
    - duration: số giây ghi âm
    - save_path: đường dẫn lưu file, nếu None thì tự tạo tên theo timestamp
    - return: đường dẫn file .wav đã lưu
    """
    print(f"Bắt đầu ghi âm trong {duration} giây...")
    
    audio_data = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16"
    )
    sd.wait()  # Chờ ghi âm xong
    print("Ghi âm xong!")

    # Tạo tên file theo timestamp nếu không truyền save_path
    if save_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("recordings", exist_ok=True)
        save_path = f"recordings/rec_{timestamp}.wav"

    wav.write(save_path, SAMPLE_RATE, audio_data)
    print(f"Đã lưu file: {save_path}")
    return save_path


def load_audio(file_path: str) -> tuple:
    """
    Load file .wav từ đường dẫn.
    - return: (sample_rate, audio_data)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")
    
    sample_rate, audio_data = wav.read(file_path)
    print(f"Đã load file: {file_path} | Sample rate: {sample_rate}Hz | Duration: {len(audio_data)/sample_rate:.2f}s")
    return sample_rate, audio_data


def list_recordings() -> list:
    """
    Liệt kê tất cả file .wav trong folder recordings/.
    """
    if not os.path.exists("recordings"):
        return []
    files = [f for f in os.listdir("recordings") if f.endswith(".wav")]
    return sorted(files, reverse=True)  # Mới nhất lên trên