# convert_audio.py
import os
import subprocess

# Danh sách convert: (file_goc, folder_dich, ten_file_moi)
CONVERT_LIST = [
    # Bộ CLEAN
    ("raw_audio/clean_01.m4a", "test_cases/clean", "sample_01.wav"),
    ("raw_audio/clean_02.m4a", "test_cases/clean", "sample_02.wav"),
    ("raw_audio/clean_03.m4a", "test_cases/clean", "sample_03.wav"),
    ("raw_audio/clean_04.m4a", "test_cases/clean", "sample_04.wav"),
    ("raw_audio/clean_05.m4a", "test_cases/clean", "sample_05.wav"),
    ("raw_audio/clean_06.m4a", "test_cases/clean", "sample_06.wav"),
    ("raw_audio/clean_07.m4a", "test_cases/clean", "sample_07.wav"),
    ("raw_audio/clean_08.m4a", "test_cases/clean", "sample_08.wav"),
    ("raw_audio/clean_09.m4a", "test_cases/clean", "sample_09.wav"),
    ("raw_audio/clean_10.m4a", "test_cases/clean", "sample_10.wav"),

    # Bộ NOISY
    ("raw_audio/noisy_01.m4a", "test_cases/noisy", "sample_01.wav"),
    ("raw_audio/noisy_02.m4a", "test_cases/noisy", "sample_02.wav"),
    ("raw_audio/noisy_03.m4a", "test_cases/noisy", "sample_03.wav"),
    ("raw_audio/noisy_04.m4a", "test_cases/noisy", "sample_04.wav"),
    ("raw_audio/noisy_05.m4a", "test_cases/noisy", "sample_05.wav"),
    ("raw_audio/noisy_06.m4a", "test_cases/noisy", "sample_06.wav"),
    ("raw_audio/noisy_07.m4a", "test_cases/noisy", "sample_07.wav"),
    ("raw_audio/noisy_08.m4a", "test_cases/noisy", "sample_08.wav"),
    ("raw_audio/noisy_09.m4a", "test_cases/noisy", "sample_09.wav"),
    ("raw_audio/noisy_10.m4a", "test_cases/noisy", "sample_10.wav"),
]

def convert():
    success = 0
    failed = 0

    for input_path, output_folder, output_name in CONVERT_LIST:
        # Kiểm tra file gốc có tồn tại không
        if not os.path.exists(input_path):
            print(f"⚠️  Không tìm thấy: {input_path} — bỏ qua")
            failed += 1
            continue

        # Tạo folder đích nếu chưa có
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, output_name)

        # Chạy FFmpeg convert
        cmd = [
            "ffmpeg", "-y",         # -y: tự ghi đè nếu file đã tồn tại
            "-i", input_path,
            "-ar", "16000",         # Sample rate 16kHz cho Whisper
            "-ac", "1",             # Mono
            "-sample_fmt", "s16",   # 16-bit
            output_path
        ]

        print(f"Converting: {input_path} → {output_path}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✓ Xong: {output_path}")
            success += 1
        else:
            print(f"✗ Lỗi: {input_path}")
            print(result.stderr[-200:])  # In 200 ký tự cuối của lỗi
            failed += 1

    print(f"\n{'='*40}")
    print(f"Kết quả: {success} thành công, {failed} thất bại")

if __name__ == "__main__":
    convert()