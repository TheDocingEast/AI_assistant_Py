import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from typing import IO
load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)
f = open("answer.txt","r")
answer = (f.read())
def text_to_speech(text: str) -> IO[bytes]:
    # Calling the text_to_speech conversion API with detailed parameters

    response = client.text_to_speech.convert(
        voice_id="ThT5KcBeYPX3keUQqHPh", # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5", # use the turbo model for low latency

        # Optional voice settings that allow you to customize the output

        voice_settings=VoiceSettings(
            stability=0.2,
            similarity_boost=1.0,
            style=0.6,
            use_speaker_boost=True,
            speed=1.0,
        ),

    )

    # uncomment the line below to play the audio back

    # play(response)

    # Generating a unique file name for the output MP3 file

    save_file_path = "answer.ogg"
    # Writing the audio to a file

    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file

    return save_file_path


text_to_speech(answer)