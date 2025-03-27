import streamlit as st
import speech_recognition as sr
import whisper
import os
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

def record_audio(filename=f"{wav_files}/user_order.wav"):
    """Records audio until silence is detected and saves it as a WAV file."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 **Listening... Speak now!**")
        recognizer.adjust_for_ambient_noise(source)  # Adapt to background noise
        audio_data = []
        
        try:
            while True:
                audio = recognizer.listen(source, phrase_time_limit=5)  # Capture speech chunks
                audio_data.append(audio.get_wav_data())  

                # Convert to text to check for silence
                try:
                    text = stt_model.transcribe(audio.get_wav_data()).get("text", "")
                    if not text.strip():  # Silence detected
                        st.write("🛑 **Silence detected. Stopping recording...**")
                        break
                except Exception:
                    pass  # Ignore errors from transcribing small silent clips

        except Exception as e:
            st.error(f"❌ Recording Error: {e}")
            return None

        # Save recorded audio
        with open(filename, "wb") as f:
            for chunk in audio_data:
                f.write(chunk)
        
        st.write("✅ **Recording saved!**")
        return filename

def transcribe_audio(filename):
    """Transcribes recorded audio using Whisper."""
    if not filename or not os.path.exists(filename):
        st.error("⚠️ No valid audio file found. Please record again.")
        return ""
    try:
        result = stt_model.transcribe(filename)
        return result.get("text", "")
    except Exception as e:
        st.error(f"❌ Transcription Error: {e}")
        return ""

def get_llm_response(user_text):
    """Gets response from the chatbot."""
    return stream_graph_updates(user_text)

def text_to_speech(response_text, max_words=50):
    """Converts text to speech and plays the response."""
    if not response_text.strip():
        st.error("⚠️ No response text provided for TTS.")
        return None
    
    words = response_text.split()
    text_chunks = [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]
    output_files = []
    
    try:
        for idx, chunk in enumerate(text_chunks):
            output_file = os.path.join(wav_files, f"order_response_{idx}.wav")
            tts_model.tts_to_file(text=chunk, file_path=output_file)
            output_files.append(output_file)
        
        for file in output_files:
            audio = AudioSegment.from_wav(file)
            play(audio)
        return output_files
    except Exception as e:
        st.error(f"❌ TTS Error: {e}")
        return None

def ai_voice_assistance():
    """Runs the AI voice assistant pipeline."""
    audio_file = record_audio()
    if audio_file:
        user_text = transcribe_audio(audio_file)
        if user_text:
            st.write(f"📝 **You said:** {user_text}")
            bot_response = get_llm_response(user_text)
            st.write(f"🤖 **Bot says:** {bot_response}")
            text_to_speech(bot_response)
    else:
        st.write("🔁 Please try recording again.")

def ai_voice_assistance():
    return record_audio, transcribe_audio, get_llm_response, text_to_speech