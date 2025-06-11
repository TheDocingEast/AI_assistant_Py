import pyaudio
import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from io import BytesIO
import wave
load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def stt(file_name):
    with open(file_name, "rb") as file:
        audio_data = file.read()
    response = audio_data
    audio = BytesIO(response)
    transcription = client.speech_to_text.convert(
        file=audio,
        model_id="scribe_v1", # Model to use, for now only "scribe_v1" is supported
        tag_audio_events=True, # Tag audio events like laughter, applause, etc.
        language_code="rus", # Language of the audio file. If set to None, the model will detect the language automatically.
        diarize=True, # Whether to annotate who is speaking

    )
    with open("file.txt", "w") as f:
        f.write(transcription.text)
    print(transcription.text)
    return transcription.text
