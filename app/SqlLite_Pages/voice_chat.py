import streamlit as st
import whisper
import wave
import os
import numpy as np
import sounddevice as sd
from dotenv import load_dotenv
from TTS.api import TTS
from bot.agent import stream_graph_updates
from pydub import AudioSegment
from pydub.playback import play

# Load environment variables
load_dotenv()

# Load Whisper STT model
stt_model = whisper.load_model("base")

# Load Coqui TTS model
tts_model = TTS("tts_models/en/ljspeech/tacotron2-DDC", gpu=False)

# Create a directory to store audio files
wav_files = os.path.abspath(os.path.join(os.path.dirname(__file__), "wav_files"))
os.makedirs(wav_files, exist_ok=True)

# ✅ Improved Function to Record Audio with Silence Detection
def record_audio(filename=f"{wav_files}/user_order.wav", samplerate=44100, duration=10, silence_threshold=500):
    st.write("🎤 Speak now... Recording until silence is detected.")
    recording = []
    
    def callback(indata, frames, time, status):
        if status:
            print(status)
        recording.append(indata.copy())

    with sd.InputStream(samplerate=samplerate, channels=1, callback=callback, dtype=np.int16) as stream:
        for _ in range(int(duration * 10)):
            sd.sleep(100)
            audio_data = np.concatenate(recording, axis=0)
            if np.max(audio_data) < silence_threshold:
                break

    wave_file = wave.open(filename, "wb")
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(samplerate)
    wave_file.writeframes(audio_data.tobytes())
    wave_file.close()
    return filename

# 📝 Function to Transcribe Audio
def transcribe_audio(filename=f"{wav_files}/user_order.wav"):
    """Transcribes recorded audio using Whisper."""
    if filename is None or not os.path.exists(filename):
        st.error("⚠️ No valid audio file found. Please record again.")
        return ""

    try:
        result = stt_model.transcribe(filename)
        return result.get("text", "")
    except Exception as e:
        st.error(f"❌ Transcription Error: {e}")
        return ""

# 🤖 Function to Get LLM Response
def get_llm_response(user_text):
    """Gets response from the chatbot."""
    return stream_graph_updates(user_text)

# 🔊 Function for Text-to-Speech
def text_to_speech(response_text, max_words=50):
    """Converts text to speech and plays the response in smaller chunks if needed."""
    if not response_text.strip():
        st.error("⚠️ No response text provided for TTS.")
        return None

    # Split long text into chunks of `max_words` words
    words = response_text.split()
    text_chunks = [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

    output_files = []
    
    try:
        for idx, chunk in enumerate(text_chunks):
            output_file = os.path.join(wav_files, f"order_response_{idx}.wav")
            tts_model.tts_to_file(text=chunk, file_path=output_file)
            output_files.append(output_file)

        # Play each chunk sequentially
        for file in output_files:
            audio = AudioSegment.from_wav(file)
            play(audio)

        return output_files
    except Exception as e:
        st.error(f"❌ TTS Error: {e}")
        return None

def ai_voice_assistance():
    return record_audio, transcribe_audio, get_llm_response, text_to_speech
