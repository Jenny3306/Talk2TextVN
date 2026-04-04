# record_test_cases.py
import os
from audio_io import record_audio

SENTENCES = [
    "Xin chào, hôm nay trời đẹp quá.",
    "Tôi đang học lập trình Python.",
    "Dự án này chạy hoàn toàn offline.",
    "Hệ thống nhận dạng giọng nói tiếng Việt.",
    "Cuộc họp bắt đầu lúc ba giờ chiều.",
    "Tôi không hiểu tại sao nó bị lỗi.",
    "Hôm nay tôi cần hoàn thành báo cáo.",
    "Mô hình học máy cần nhiều dữ liệu.",
    "Ứng dụng này bảo vệ quyền riêng tư.",
    "Kết quả thử nghiệm rất khả quan.",
]

def record_set(folder: str, label: str):
    os.makedirs(folder, exist_ok=True)
    print(f"\n{'='*55}")
    print(f"Bộ test: {label}")
    print(f"Lưu vào: {folder}")
    print(f"{'='*55}")

    for i, sentence in enumerate(SENTENCES, 1):
        print(f"\n[{i}/10] Câu cần nói:")
        print(f"  → {sentence}")
        input("Nhấn Enter khi sẵn sàng (ghi 4 giây)...")

        save_path = os.path.join(folder, f"sample_{i:02d}.wav")
        record_audio(duration=4, save_path=save_path)
        print(f"✓ Đã lưu: {save_path}")

    print(f"\n✓ Xong bộ {label}!")


# Thu âm bộ clean trước
record_set("test_cases/clean", "CLEAN — Nói rõ, phòng yên tĩnh")

print("\n" + "="*55)
print("Nghỉ 1 phút, chuẩn bị bộ NOISY")
print("Bật nhạc nền nhỏ hoặc chuẩn bị nói nhanh hơn")
input("Nhấn Enter khi sẵn sàng tiếp...")

# Thu âm bộ noisy
record_set("test_cases/noisy", "NOISY — Có tiếng ồn hoặc nói nhanh")

print("\n✓ Hoàn thành thu âm toàn bộ test cases!")