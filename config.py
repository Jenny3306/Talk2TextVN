# config.py

# Model Whisper: "tiny" (nhanh nhất), "base", "small", "medium", "large"
WHISPER_MODEL = "base"

# Ngôn ngữ
LANGUAGE = "vi"

# Audio settings
SAMPLE_RATE = 16000      # Hz, Whisper yêu cầu 16kHz
CHANNELS = 1             # Mono
RECORD_SECONDS = 8      # Thời gian ghi âm mặc định

# Text post-processing
ENABLE_PUNCTUATION = True
ENABLE_LINE_BREAKS = True
ENABLE_FILLER_REMOVAL = True

# Paths
TEST_CASES_DIR = "test_cases"
RESULTS_DIR = "results"