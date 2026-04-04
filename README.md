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
```
Audio Capture → Preprocessing → Whisper STT → Text Normalization → Evaluation → UI
```

**Pipeline stages:**
1. **Audio Capture** — Record from microphone or load file (.wav, .mp3, .m4a)
2. **Preprocessing** — Resample to 16kHz, convert to mono, trim silence, normalize to float32
3. **Whisper STT** — Transcribe Vietnamese speech using Whisper Tiny (on-device)
4. **Text Normalization** — Three methods: rule-based, Gemma API, Gemma on-device (Ollama)
5. **Evaluation** — WER/CER measurement, latency logging, error analysis
6. **Demo UI** — Streamlit interface with real-time transcription

---

## 🤖 About Gemma 3n

**Gemma 3n** is Google's multimodal AI model optimized for on-device applications. In Talk2TextVN, Gemma 3n serves as the **text normalization engine** — the component responsible for understanding Vietnamese semantics and improving transcript readability.

### Why Gemma 3n?

| Feature | Benefit for Talk2TextVN |
|---------|------------------------|
| On-device inference | Runs locally via Ollama — no cloud dependency |
| Multilingual capability | Understands Vietnamese semantics and context |
| Lightweight architecture | Efficient enough for CPU-only machines |
| Instruction-following | Follows normalization rules precisely |

### Integration Approach

Talk2TextVN integrates Gemma 3n in two modes:

**Mode 1 — Gemma API** (via Google AI Studio)
- Fast response: 3–5s per request
- Requires internet connection
- Best for development and testing

**Mode 2 — Gemma Local** (via Ollama, fully offline)
- First-run warmup: ~62s (model loading into RAM)
- Subsequent runs: 4–7s
- No internet required — true privacy-first inference
- Requires 8GB+ RAM

### What Gemma 3n adds over rule-based
```
Input (Whisper raw):  "xin chào tôi tên là nam hôm nay trời đẹp quá"
Rule-based output:    "Xin chào tôi tên là nam hôm nay trời đẹp quá."
Gemma 3n output:      "Xin chào, tôi tên là Nam. Hôm nay trời đẹp quá!"
```
Gemma 3n correctly:
- Capitalizes proper nouns (`nam` → `Nam`)
- Adds contextually appropriate punctuation (`,` and `!`)
- Understands sentence boundaries semantically

---

## 📊 Benchmark Results

Evaluated on 20 real-world Vietnamese audio samples (10 clean, 10 noisy).

### Transcription Quality (Whisper Tiny)

| Condition | Avg WER | Avg CER | Avg Latency |
|-----------|---------|---------|-------------|
| Clean     | 0.65    | 0.45    | 3.06s       |
| Noisy     | 0.78    | 0.55    | 2.60s       |
| Noise degradation | +20.3% | — | — |

### Post-processing Comparison

| Method | WER (clean) | WER (noisy) | Avg Latency |
|--------|-------------|-------------|-------------|
| Rule-based | 0.67 | 0.78 | ~0s |
| Gemma API | 0.67 | 0.78 | 3–5s |
| Gemma Local (Ollama) | — | — | 4–7s |

### Key Findings
- Whisper Tiny correctly recognizes **3/10 clean sentences** (WER < 0.3)  
- Background noise increases WER by **20.3%**  
- Gemma improves semantic errors that rule-based methods cannot handle (e.g., proper nouns, context-aware punctuation)  
- Gemma Local performance: ~62s warmup on first run, **4–7s** on subsequent runs  

---

## 🔍 Error Analysis  

### What Whisper Tiny handles well  
- Short sentences with clear pronunciation in quiet environments  
- Common vocabulary without complex proper nouns  

### Common failure cases  
- Background noise → model hallucinates into other languages (Korean, Greek, German)  
- Technical terms: “Python”, “offline”, “machine learning” → often misrecognized  
- Long sentences (> 8 words) → significantly higher WER  
- Non-standard accents → output contains mixed Unicode characters from multiple languages  

### What post-processing fixes  
- ✅ Capitalization of sentence beginnings and proper nouns (Gemma)  
- ✅ Context-aware punctuation (Gemma)  
- ✅ Removal of filler words: “uhm”, “uh”, “well”, etc.  
- ✅ Correction of abbreviations: “ko” → “không”, “dc” → “được”, “mn” → “mọi người”  

### What post-processing cannot fix  
- ❌ Completely incorrect language output from Whisper  
- ❌ Hallucinated or corrupted Unicode characters  
- ❌ Lack of context to recover misrecognized words  

---

## 🛠️ Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Speech Recognition | Whisper Tiny | Vietnamese STT, on-device |
| Text Normalization | Rule-based module | Fast, zero-latency baseline |
| Text Normalization | Gemma 3n (Google AI API) | Semantic understanding |
| Text Normalization | Gemma 3n (Ollama) | Fully offline inference |
| Audio Processing | SciPy, NumPy | Resample, normalize, trim |
| Evaluation | jiwer | WER/CER measurement |
| Demo UI | Streamlit | Interactive web interface |
| Language | Python 3.11 | Backend |

---

## 🚀 Installation

### Prerequisites
- Python 3.11
- FFmpeg ([download](https://ffmpeg.org/download.html))
- Ollama ([download](https://ollama.com)) — optional, for on-device Gemma

### Setup
```bash
# 1. Clone repository
git clone https://github.com/Jenny3306/Talk2TextVN.git
cd Talk2TextVN

# 2. Create virtual environment with Python 3.11
py -3.11 -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup API key (optional, for Gemma API)
cp .env.example .env
# Edit .env and add your GEMMA_API_KEY

# 5. Pull Gemma model (optional, for on-device inference)
ollama pull gemma3n
```

### Run
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## 📁 Project Structure
```
talk2textvn/
├── audio_io.py          # Audio recording and loading
├── preprocess.py        # Audio preprocessing pipeline
├── transcribe.py        # Whisper inference + latency logging
├── postprocess.py       # Text normalization (rule-based + Gemma)
├── evaluate.py          # WER/CER evaluation + error analysis
├── app.py               # Streamlit demo UI
├── config.py            # Model and pipeline configuration
├── test_cases/
│   ├── clean/           # 10 audio samples, quiet environment
│   │   └── ground_truth.txt
│   └── noisy/           # 10 audio samples, noisy environment
│       └── ground_truth.txt
├── results/             # Benchmark outputs (JSON + CSV)
├── .env.example         # API key template
└── requirements.txt     # Dependencies
```
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

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Jenny3306** · [github.com/Jenny3306](https://github.com/Jenny3306)
