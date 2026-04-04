# app.py
import streamlit as st
import tempfile
import os
import time
from audio_io import record_audio
from preprocess import preprocess
from transcribe import transcribe
from postprocess import postprocess

# ── Cấu hình trang ────────────────────────────────────────────
st.set_page_config(
    page_title="Talk2TextVN",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Talk2TextVN")
st.caption("Offline Vietnamese Speech-to-Text · Powered by Whisper + Gemma 3n")

# ── Sidebar settings ───────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Cài đặt")
    duration = st.slider("Thời gian ghi âm (giây)", 3, 15, 5)
    method = st.radio(
        "Phương pháp post-processing",
        ["Rule-based", "Gemma API", "Gemma Local (Ollama)"],
        index=0
    )
    st.divider()
    st.markdown("**Thông tin model:**")
    st.markdown("- STT: Whisper Tiny")
    st.markdown("- NLP: Gemma 3n")
    st.markdown("- Mode: Offline")

# ── Tab chính ─────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🎤 Ghi âm trực tiếp", "📁 Upload file"])

# Tab 1: Ghi âm
with tab1:
    st.markdown("Nhấn nút bên dưới để bắt đầu ghi âm tiếng Việt.")

    if st.button("🔴 Bắt đầu ghi âm", type="primary", use_container_width=True):
        with st.spinner(f"Đang ghi âm {duration} giây..."):
            audio_path = record_audio(duration=duration)

        st.audio(audio_path)
        st.success("Ghi âm xong!")

        with st.spinner("Đang nhận dạng giọng nói..."):
            audio_data = preprocess(audio_path)
            result = transcribe(audio_data)

        with st.spinner("Đang chuẩn hóa văn bản..."):
            use_gemma = method == "Gemma API"
            use_local = method == "Gemma Local (Ollama)"
            post = postprocess(result["raw_text"], use_gemma=use_gemma, use_local=use_local)

        # Hiển thị kết quả
        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("⏱️ Latency", f"{result['latency_s']}s")
        col2.metric("🤖 Model", result["model"])
        col3.metric("🔧 Method", post["method"])

        st.markdown("**📝 Raw transcript (Whisper):**")
        st.info(result["raw_text"] if result["raw_text"] else "_(không nhận dạng được)_")

        st.markdown("**✨ Cleaned text (sau post-processing):**")
        st.success(post["cleaned_text"] if post["cleaned_text"] else "_(trống)_")

        # Copy button
        st.code(post["cleaned_text"], language=None)

# Tab 2: Upload file
with tab2:
    uploaded = st.file_uploader(
        "Upload file audio (.wav, .mp3, .m4a)",
        type=["wav", "mp3", "m4a"]
    )

    if uploaded:
        # Lưu file gốc vào temp
        suffix = "." + uploaded.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded.read())
            tmp_path = tmp.name

        # Convert sang .wav nếu không phải .wav
        if suffix.lower() != ".wav":
            import subprocess
            wav_path = tmp_path.replace(suffix, ".wav")
            with st.spinner("Đang convert sang .wav..."):
                subprocess.run([
                    "ffmpeg", "-y",
                    "-i", tmp_path,
                    "-ar", "16000",
                    "-ac", "1",
                    "-sample_fmt", "s16",
                    wav_path
                ], capture_output=True)
            os.unlink(tmp_path)   # Xóa file gốc
            tmp_path = wav_path   # Dùng file .wav mới

        st.audio(tmp_path)

        if st.button("▶️ Nhận dạng", type="primary", use_container_width=True):
            with st.spinner("Đang xử lý..."):
                audio_data = preprocess(tmp_path)
                result = transcribe(audio_data)
                use_gemma = method == "Gemma API"
                use_local = method == "Gemma Local (Ollama)"
                post = postprocess(result["raw_text"], use_gemma=use_gemma, use_local=use_local)

            st.divider()
            col1, col2, col3 = st.columns(3)
            col1.metric("⏱️ Latency", f"{result['latency_s']}s")
            col2.metric("🤖 Model", result["model"])
            col3.metric("🔧 Method", post["method"])

            st.markdown("**📝 Raw transcript:**")
            st.info(result["raw_text"] if result["raw_text"] else "_(không nhận dạng được)_")

            st.markdown("**✨ Cleaned text:**")
            st.success(post["cleaned_text"] if post["cleaned_text"] else "_(trống)_")

            st.code(post["cleaned_text"], language=None)

            os.unlink(tmp_path)

# ── Footer ─────────────────────────────────────────────────────
st.divider()
st.caption("Talk2TextVN · MIT License · github.com/Jenny3306/talk2textvn")