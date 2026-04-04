# evaluate.py
import os
import json
import time
import csv
from jiwer import wer, cer
from transcribe import transcribe
from preprocess import preprocess
from postprocess import postprocess

def evaluate_set(audio_folder: str, ground_truth_file: str, label: str) -> list:
    """
    Đánh giá toàn bộ một bộ test:
    - Transcribe từng file audio
    - So sánh với ground truth
    - Tính WER/CER trước và sau post-processing
    - Log latency
    """
    # Load ground truth
    with open(ground_truth_file, "r", encoding="utf-8") as f:
        references = [line.strip() for line in f.readlines() if line.strip()]

    # Lấy danh sách file audio
    audio_files = sorted([
        f for f in os.listdir(audio_folder) if f.endswith(".wav")
    ])

    if len(audio_files) != len(references):
        print(f"⚠️ Số file audio ({len(audio_files)}) != số ground truth ({len(references)})")

    results = []

    print(f"\n{'='*55}")
    print(f"Đánh giá bộ: {label}")
    print(f"{'='*55}")

    for i, (audio_file, reference) in enumerate(zip(audio_files, references), 1):
        audio_path = os.path.join(audio_folder, audio_file)
        print(f"\n[{i}] {audio_file}")

        # Preprocess + Transcribe
        audio_data = preprocess(audio_path)
        trans = transcribe(audio_data)
        raw_text = trans["raw_text"].lower()

        # Post-process (rule-based)
        post_rule = postprocess(raw_text, use_gemma=False)
        cleaned_rule = post_rule["cleaned_text"].lower()

        # Post-process (Gemma API)
        post_gemma = postprocess(raw_text, use_gemma=True)
        cleaned_gemma = post_gemma["cleaned_text"].lower()

        # Tính metrics
        wer_raw   = round(wer(reference, raw_text), 4)
        wer_rule  = round(wer(reference, cleaned_rule), 4)
        wer_gemma = round(wer(reference, cleaned_gemma), 4)
        cer_raw   = round(cer(reference, raw_text), 4)

        result = {
            "file": audio_file,
            "reference": reference,
            "raw_text": raw_text,
            "cleaned_rule": cleaned_rule,
            "cleaned_gemma": cleaned_gemma,
            "wer_raw": wer_raw,
            "wer_rule": wer_rule,
            "wer_gemma": wer_gemma,
            "cer_raw": cer_raw,
            "latency_s": trans["latency_s"],
        }
        results.append(result)

        print(f"    Ref    : {reference}")
        print(f"    Raw    : {raw_text}  (WER: {wer_raw})")
        print(f"    Rule   : {cleaned_rule}  (WER: {wer_rule})")
        print(f"    Gemma  : {cleaned_gemma}  (WER: {wer_gemma})")
        print(f"    Latency: {trans['latency_s']}s")

    return results


def save_results(results: list, label: str):
    """Lưu kết quả ra JSON và CSV."""
    os.makedirs("results", exist_ok=True)
    base = f"results/eval_{label.lower().replace(' ', '_')}"

    # JSON
    with open(f"{base}.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # CSV
    with open(f"{base}.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✓ Đã lưu: {base}.json và {base}.csv")


def print_summary(results: list, label: str):
    """In bảng tổng kết."""
    avg_wer_raw   = round(sum(r["wer_raw"]   for r in results) / len(results), 4)
    avg_wer_rule  = round(sum(r["wer_rule"]  for r in results) / len(results), 4)
    avg_wer_gemma = round(sum(r["wer_gemma"] for r in results) / len(results), 4)
    avg_cer       = round(sum(r["cer_raw"]   for r in results) / len(results), 4)
    avg_latency   = round(sum(r["latency_s"] for r in results) / len(results), 3)

    improve_rule  = round((avg_wer_raw - avg_wer_rule)  / avg_wer_raw * 100, 1) if avg_wer_raw > 0 else 0
    improve_gemma = round((avg_wer_raw - avg_wer_gemma) / avg_wer_raw * 100, 1) if avg_wer_raw > 0 else 0

    print(f"\n{'='*55}")
    print(f"TỔNG KẾT — {label}")
    print(f"{'='*55}")
    print(f"  Avg WER (raw)        : {avg_wer_raw}")
    print(f"  Avg WER (rule-based) : {avg_wer_rule}  (cải thiện {improve_rule}%)")
    print(f"  Avg WER (gemma)      : {avg_wer_gemma}  (cải thiện {improve_gemma}%)")
    print(f"  Avg CER (raw)        : {avg_cer}")
    print(f"  Avg latency          : {avg_latency}s")

def error_analysis(clean_results: list, noisy_results: list):
    """
    Phân tích lỗi so sánh giữa clean và noisy.
    In ra các failure cases và pattern lỗi phổ biến.
    """
    print(f"\n{'='*55}")
    print("ERROR ANALYSIS")
    print(f"{'='*55}")

    # 1. So sánh WER clean vs noisy
    clean_wer = sum(r["wer_raw"] for r in clean_results) / len(clean_results)
    noisy_wer = sum(r["wer_raw"] for r in noisy_results) / len(noisy_results)
    degradation = round((noisy_wer - clean_wer) / clean_wer * 100, 1)

    print(f"\n[1] Tác động của noise:")
    print(f"    WER clean : {round(clean_wer, 4)}")
    print(f"    WER noisy : {round(noisy_wer, 4)}")
    print(f"    Độ giảm   : {degradation}% khi có noise")

    # 2. Các câu Whisper nhận dạng hoàn toàn sai (WER >= 1.0)
    clean_failures = [r for r in clean_results if r["wer_raw"] >= 1.0]
    noisy_failures = [r for r in noisy_results if r["wer_raw"] >= 1.0]

    print(f"\n[2] Failure cases (WER >= 1.0):")
    print(f"    Clean: {len(clean_failures)}/10 câu")
    print(f"    Noisy: {len(noisy_failures)}/10 câu")

    # 3. Các câu Whisper nhận dạng tốt (WER < 0.3)
    clean_good = [r for r in clean_results if r["wer_raw"] < 0.3]
    noisy_good = [r for r in noisy_results if r["wer_raw"] < 0.3]

    print(f"\n[3] Câu nhận dạng tốt (WER < 0.3):")
    print(f"    Clean: {len(clean_good)}/10 câu")
    print(f"    Noisy: {len(noisy_good)}/10 câu")
    for r in clean_good:
        print(f"    ✓ '{r['reference']}' → WER {r['wer_raw']}")

    # 4. Gemma giúp ích ở đâu
    gemma_improved_clean = [
        r for r in clean_results if r["wer_gemma"] < r["wer_raw"]
    ]
    gemma_improved_noisy = [
        r for r in noisy_results if r["wer_gemma"] < r["wer_raw"]
    ]

    print(f"\n[4] Gemma cải thiện được:")
    print(f"    Clean: {len(gemma_improved_clean)}/10 câu")
    print(f"    Noisy: {len(gemma_improved_noisy)}/10 câu")
    for r in gemma_improved_clean:
        print(f"    ↑ '{r['raw_text']}' → WER {r['wer_raw']} → {r['wer_gemma']}")

    # 5. Kết luận
    print(f"\n[5] Kết luận:")
    print(f"    - Whisper Tiny hoạt động tốt với câu ngắn, rõ ràng")
    print(f"    - Noise làm WER tăng {degradation}%")
    print(f"    - Gemma cải thiện {len(gemma_improved_clean)} câu ở bộ clean")
    print(f"    - Cần model lớn hơn (base/small) cho môi trường có noise")
    print(f"    - Failure cases chủ yếu do: giọng không rõ, tiếng ồn lớn")