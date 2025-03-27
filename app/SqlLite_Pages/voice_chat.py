import streamlit as st
import whisper, sounddevice as sd, numpy as np, wave, os, dotenv
from TTS.api import TTS
from bot.agent import stream_graph_updates

dotenv.load_dotenv()

# Load Whisper STT model
stt_model = whisper.load_model("base")

# Load Coqui TTS model
tts_model = TTS("tts_models/en/ljspeech/tacotron2-DDC", gpu=False)

wav_files = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SqlLite_Pages", "wav_files"))
os.makedirs(wav_files, exist_ok=True)

def record_audio(filename=f"{wav_files}/user_order.wav", samplerate=44100, duration=10, silence_threshold=500):
    st.write("🎤 Speak now... Recording until silence is detected.")

    recording = []
    
    def callback(indata, frames, time, status):
        if status:
            print(status)
        recording.append(indata.copy())

    with sd.InputStream(samplerate=samplerate, channels=1, callback=callback, dtype=np.int16) as stream:
        for _ in range(int(duration * 10)):  # Record in small chunks
            sd.sleep(100)
            audio_data = np.concatenate(recording, axis=0)
            if np.max(audio_data) < silence_threshold:  # Stop if silence is detected
                break

    # Save recorded audio
    wave_file = wave.open(filename, "wb")
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(samplerate)
    wave_file.writeframes(audio_data.tobytes())
    wave_file.close()

    return filename

def transcribe_audio(filename=f"{wav_files}/user_order.wav"):
    result = stt_model.transcribe(filename)
    return result["text"]

def get_llm_response(user_text):
    return stream_graph_updates(user_text)

def text_to_speech(response_text, output_file=f"{wav_files}/order_response.wav"):
    tts_model.tts_to_file(text=response_text, file_path=output_file)
    os.system(f"aplay {output_file}")
    return output_file

def ai_voice_assistance():
    return record_audio, transcribe_audio, get_llm_response, text_to_speech