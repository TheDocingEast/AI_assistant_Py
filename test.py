import flet as ft
import pyaudio
import wave
import threading
import audioget
import answer_generate
import logging
import hashlib
import uuid
from dotenv import load_dotenv
load_dotenv()
import os
from gigachat import GigaChat

uuid_page = str(uuid.uuid4())
giga = GigaChat(
credentials=os.getenv("GIGACHAT_API_KEY"),
verify_ssl_certs=False,
)

res = giga.get_token()
access_token = res.access_token
context_headers = {
    "X-Session-ID": uuid_page,
}
print(res)
print(access_token)