
import uuid
import gigachat.context
from gigachat import GigaChat
import os
from dotenv import load_dotenv
load_dotenv()
def generate_answer(message: str, headers: dict):
    with GigaChat(
        credentials=os.getenv("GIGACHAT_API_KEY"),
        verify_ssl_certs=False
    ) as giga:
        gigachat.context.session_id_cvar.set(headers.get("X-Session-ID"))

    response = giga.chat(message)
    print(response.choices[0].message.content)
    return response.choices[0].message.content
print(uuid.uuid4())