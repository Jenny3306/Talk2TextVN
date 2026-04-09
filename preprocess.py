# preprocess.py
# Chức năng: chuẩn hóa audio trước khi đưa vào Whisper

import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal
import os
from config import SAMPLE_RATE

def resample_audio(audio_data: np.ndarray, orig_rate: int, target_rate: int = SAMPLE_RATE) -> np.ndarray:
    """
    Resample audio về đúng sample rate mà Whisper yêu cầu (16000 Hz).
    """
    if orig_rate == target_rate:
        return audio_data  # Không cần resample
    
    num_samples = int(len(audio_data) * target_rate / orig_rate)
    resampled = signal.resample(audio_data, num_samples)
    return resampled.astype(np.int16)


def normalize_audio(audio_data: np.ndarray) -> np.ndarray:
    """
    Normalize biên độ audio về khoảng [-1, 1] dạng float32.
    Whisper cần input dạng float32 normalized.
    """
    audio_float = audio_data.astype(np.float32)
    max_val = np.max(np.abs(audio_float))
    if max_val == 0:
        return audio_float  # Tránh chia cho 0 (audio im lặng)
    return audio_float / max_val


def trim_silence(audio_data: np.ndarray, threshold: float = 0.001) -> np.ndarray:
    """
    Cắt bỏ khoảng im lặng ở đầu và cuối file audio.
    - threshold: ngưỡng biên độ coi là im lặng (0.0 - 1.0)
    """
    audio_norm = normalize_audio(audio_data)
    # Tìm vị trí đầu tiên và cuối cùng có âm thanh vượt ngưỡng
    non_silent = np.where(np.abs(audio_norm) > threshold)[0]
    
    if len(non_silent) == 0:
        print("Cảnh báo: File audio có vẻ hoàn toàn im lặng.")
        return audio_data
    
    start = max(0, non_silent[0] - 1000)       # Giữ lại 1000 sample trước
    end = min(len(audio_data), non_silent[-1] + 1000)  # Và sau phần có âm thanh
    return audio_data[start:end]


def preprocess(file_path: str, denoise: bool = True) -> np.ndarray:
    """
    Pipeline tiền xử lý đầy đủ cho một file audio.
    Chạy theo thứ tự: load → resample → trim silence → normalize
    - return: audio dạng float32, sẵn sàng đưa vào Whisper
    """
    # 1. Load file
    orig_rate, audio_data = wav.read(file_path)
    
    # 2. Convert int32 → int16 nếu cần
    if audio_data.dtype == np.int32:
        audio_data = (audio_data / 65536).astype(np.int16)
    elif audio_data.dtype == np.float64:
        audio_data = (audio_data * 32767).astype(np.int16)

    # 3. Convert stereo → mono nếu cần
    if len(audio_data.shape) == 2:
        audio_data = audio_data.mean(axis=1).astype(np.int16)
    
    # 4. Resample về 16kHz
    audio_data = resample_audio(audio_data, orig_rate)
    
    # 5. Cắt im lặng
    # audio_data = trim_silence(audio_data)
    
    # 6. Normalize về float32
    audio_data = normalize_audio(audio_data)

    # 7. Noise reduction (chỉ áp dụng nếu denoise=True)
    # if denoise:
    #    print("Đang giảm tiếng ồn...")
    #    audio_data = reduce_noise(audio_data)
    
    duration = len(audio_data) / SAMPLE_RATE
    print(f"Preprocess xong | Duration sau xử lý: {duration:.2f}s")
    return audio_data