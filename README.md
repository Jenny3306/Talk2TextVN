# 🎙️ Talk2TextVN

> An offline Vietnamese speech recognition pipeline combining Whisper-based transcription with Gemma 3n post-processing for punctuation restoration, text normalization, and improved readability.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Whisper](https://img.shields.io/badge/Whisper-Tiny-purple)](https://github.com/openai/whisper)
[![Gemma](https://img.shields.io/badge/Gemma-3n-orange)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🎯 Project Goal

Talk2TextVN is an **on-device Vietnamese speech recognition system** designed for privacy-preserving, offline transcription. The project focuses on building a practical speech pipeline from audio capture to transcription and text normalization, with emphasis on latency, readability, and robustness under real-world Vietnamese speech conditions.

**Target users:**
- Older adults who have difficulty typing
- People with hearing impairments needing real-time transcription
- Users unfamiliar with typing who prefer voice input

---

## 🏗️ System Architecture
talk2textvn/
├── audio_io.py          # Audio recording and loading
├── preprocess.py        # Audio preprocessing pipeline
├── transcribe.py        # Whisper inference + latency logging
├── postprocess.py       # Text normalization (rule-based + Gemma)
├── evaluate.py          # WER/CER evaluation + error analysis
├── app.py               # Streamlit demo UI
├── config.py            # Model and pipeline configuration
├── convert_audio.py     # Batch audio format conversion
├── test_cases/
│   ├── clean/           # 10 audio samples, quiet environment
│   │   └── ground_truth.txt
│   └── noisy/           # 10 audio samples, noisy environment
│       └── ground_truth.txt
├── results/             # Benchmark outputs (JSON + CSV)
├── recordings/          # Recorded audio files
├── .env.example         # API key template
└── requirements.txt     # Dependencies

---

## ⚙️ Configuration

Edit `config.py` to adjust pipeline behavior:
```python
WHISPER_MODEL = "tiny"    # Options: tiny, base, small, medium, large
LANGUAGE = "vi"
SAMPLE_RATE = 16000
RECORD_SECONDS = 10
ENABLE_PUNCTUATION = True
ENABLE_LINE_BREAKS = True
ENABLE_FILLER_REMOVAL = True
```

---

## 📋 Limitations

- **Whisper Tiny** trades accuracy for speed — WER 0.65 on clean speech
- **Noisy environments** significantly degrade performance (+20.3% WER)
- **Technical terms** (Python, offline, ML) often misrecognized in Vietnamese context
- **Gemma API** requires internet connection — not fully offline
- **Gemma Local** requires 8GB+ RAM and significant warmup time on first run

---

## 🔮 Future Work

- Upgrade to Whisper Base/Small for better accuracy
- Fine-tune Whisper on Vietnamese dataset (Common Voice VI)
- Add speaker diarization for multi-speaker scenarios
- Extend to speech-to-structured notes
- Build voice input for AI assistant integration
- Support real-time streaming transcription

---

## 👥 Target Audience

- **Older adults** — voice-based alternative to typing
- **People with hearing impairments** — real-time transcription tool
- **Users unfamiliar with typing** — hands-free text input

---

## 🤝 Contributing

Feel free to fork the repository, create pull requests, or open issues for bugs and feature requests.

---

## 📝 License

This project is licensed under the MIT License.

---

## 👤 Author

**Jeny3306** · [github.com/Jeny3306](https://github.com/Jeny3306)