import asyncio
import logging
from aiogram import Bot, Dispatcher, types
import answer_generate
import audioget
from aiogram.types import FSInputFile
import audioplay
from dotenv import load_dotenv
import os
load_dotenv()

# Initial bot from dotenv token
bot = Bot(token=os.getenv('TELEGRAM_API_KEY'))
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# Make response for message
@dp.message()
async def text_processing(message: types.Message):
    # Command /start send welcome message 
    if message.text and message.text.startswith("/start"):
        await message.answer("Привет, я AI-ассистент, могу ответить на вопрос какой ты мне задашь, а принимаю как текствые, так и голосовые сообщения, буду рад пообщаться!")
    # If message is voice, we send his to stt script before sending him to generate answer
    elif message.voice:
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_name = "audio.ogg"
        await bot.download_file(file_path, file_name)
        stt_answer = audioget.stt(file_name)
        # Generate answer after stt our voice message
        answer = answer_generate.generate_answer(stt_answer)
        # Generate audio answer for user
        audioplay.text_to_speech(answer)
        audio_file = FSInputFile('answer.ogg')  # Укажите путь к вашему аудиофайлу
        # Send audio message for user
        await message.answer_audio(audio=audio_file)
    # If message is text, we generate answer and send it to user
    elif message.text:
        answer = answer_generate.generate_answer(message.text)
        await message.answer(answer)

# Cycle for bot polling
async def main():
    await dp.start_polling(bot)
# Register the voice message handler
if __name__ == '__main__':
    asyncio.run(main())