import flet as ft
import pyaudio
import wave
import threading
import audioget
import answer_generate
import logging
import hashlib
import uuid

logging.basicConfig(level=logging.INFO)
def record_audio(page, device_index, recording_indicator):
    try:
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "audio.wav"

        p = pyaudio.PyAudio()

        # Открываем поток с выбранным устройством
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=device_index,
                        frames_per_buffer=CHUNK)

        frames = []

        recording_indicator.visible = True
        page.update()
        
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        recording_indicator.visible = False
        page.update()
        # Распознавание речи
        stt_answer = audioget.stt(WAVE_OUTPUT_FILENAME)
        page.controls.append(ft.Row(
            controls=[
                ft.Image(
                    src="user_avatar.jpg",
                    width=30,
                    height=30,
                    border_radius=ft.border_radius.all(15)
                ),
                ft.Container(
                    content=ft.Text(f"Вы сказали: {stt_answer}", width=200),
                    padding=10,
                    border_radius=10,
                    bgcolor="lightblue"
                )
            ]
        ))

        # Генерация ответа
        answer = answer_generate.generate_answer(stt_answer)
        page.controls.append(ft.Row(
            controls=[
                ft.Image(
                    src="AI_avatar.jpg",
                    width=30,
                    height=30,
                    border_radius=ft.border_radius.all(15)
                ),
                ft.Container(
                    content=ft.Text(f"Ответ: {answer}", width=200),
                    padding=10,
                    border_radius=10,
                    bgcolor="lightgreen"
                )
            ]
        ))
        page.update()

    except Exception as e:
        print(f"Ошибка: {e}")
        page.controls.append(ft.Text(f"Ошибка: {e}"))
        page.update()
    finally:
        # Ensure recording indicator is always hidden after recording
        recording_indicator.visible = False
        page.update()

def send_text(page, text_field):
    try:
        text = text_field.value
        if text:
            page.controls.append(ft.Row(
                controls=[
                    ft.Image(
                    src="user_avatar.jpg",
                    width=30,
                    height=30,
                    border_radius=ft.border_radius.all(15)
                ),
                    ft.Container(
                        content=ft.Text(f"Вы написали: {text}", width=200),
                        padding=10,
                        border_radius=10,
                        bgcolor="lightblue"
                    )
                ]
            ))

            # Генерация ответа
            answer = answer_generate.generate_answer(text)
            page.controls.append(ft.Row(
                controls=[
                    ft.Image(
                    src="AI_avatar.jpg",
                    width=30,
                    height=30,
                    border_radius=ft.border_radius.all(15)
                ),
                    ft.Container(
                        content=ft.Text(f"Ответ: {answer}", width=200),
                        padding=10,
                        border_radius=10,
                        bgcolor="lightgreen"
                    )
                ]
            ))
            text_field.value = ""
            page.update()

    except Exception as e:
        print(f"Ошибка: {e}")
        page.controls.append(ft.Text(f"Ошибка: {e}"))
        page.update()


def hash_password(password):
    # Генерируем случайную соль
    salt = uuid.uuid4().hex
    # Хешируем пароль с солью
    hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()
    # Возвращаем хеш и соль
    return f"{hashed_password}:{salt}"

def check_password(hashed_password, user_password):
    # Разделяем хеш и соль
    password, salt = hashed_password.split(":")
    # Хешируем введенный пароль с той же солью
    new_hash = hashlib.sha256((salt + user_password).encode()).hexdigest()
    # Сравниваем хеши
    return password == new_hash

# Хешируем пароль для проверки
stored_hashed_password = 'c8cc6a106723bd6279c2d74177c4d3d9092289934a55cc76b86f6d7c491be89c:674ceb2c2d8a4dec9a038f8e5e6080ad'  # Заданный пароль

def main(page: ft.Page):
    page.adaptive = True
    page.title = "Вход"

    def check_password_in_interface(e):
        # Получаем пароль от пользователя
        user_password = password_field.value

        if check_password(stored_hashed_password, user_password):
            # Пароль верный, переходите к основному интерфейсу
            page.controls.clear()
            main_page(page)
        else:
            # Пароль неверный, показываем ошибку
            page.controls.append(ft.Text("Неправильный пароль"))

    password_field = ft.TextField(
        label="Введите пароль",
        password=True,
        can_reveal_password=True,
        width=300
    )
    container = ft.Container(
        content = ft.Column(
            controls=[
                password_field,
                ft.ElevatedButton("Войти", on_click=check_password_in_interface)
            ],
            alignment="center"
        ),
        padding=ft.padding.only(top=50)
    )
    page.add(container)

import flet as ft

def main_page(page: ft.Page):
    page.adaptive = True
    page.title = "Чат"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # Создаем прокручиваемый столбец для чата
    chat = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,  # Включаем прокрутку
        expand=True,  # Занимаем всю доступную высоту
    )

    text_field = ft.TextField(hint_text="Введите текст", width=300)

    recording_indicator = ft.Text("Запись...", visible=False, color=ft.Colors.WHITE)

    def send_click(e):
        send_text(page, text_field)

    def record_click(e):
        threading.Thread(target=record_audio, args=(page,)).start()

    def add_message(message):
        chat.controls.append(message)
        page.update()

    def record_audio_thread(page):
        try:
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            RECORD_SECONDS = 5
            WAVE_OUTPUT_FILENAME = "audio.wav"

            p = pyaudio.PyAudio()

            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

            frames = []

            recording_indicator.visible = True
            page.update()
            
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            stream.stop_stream()
            stream.close()
            p.terminate()

            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            recording_indicator.visible = False
            page.update()
            
            # Распознавание речи
            stt_answer = audioget.stt(WAVE_OUTPUT_FILENAME)
            add_message(ft.Row(
                controls=[
                    ft.Image(
                    src="user_avatar.jpg",
                    width=30,
                    height=30,
                    border_radius=ft.border_radius.all(15)
                ),
                    ft.Container(
                        content=ft.Text(f"Вы сказали: {stt_answer}", width=200),
                        padding=10,
                        border_radius=10,
                        bgcolor="lightblue"
                    )
                ]
            ))

            # Генерация ответа
            answer = answer_generate.generate_answer(stt_answer)
            add_message(ft.Row(
                controls=[
                    ft.Image(
                    src="AI_avatar.jpg",
                    width=30,
                    height=30,
                    border_radius=ft.border_radius.all(15)
                ),
                    ft.Container(
                        content=ft.Text(f"Ответ: {answer}", width=200),
                        padding=10,
                        border_radius=10,
                        bgcolor="lightgreen"
                    )
                ]
            ))

        except Exception as e:
            print(f"Ошибка: {e}")
            add_message(ft.Text(f"Ошибка: {e}"))
        finally:
             # Ensure recording indicator is always hidden after recording
            recording_indicator.visible = False
            page.update()
            
    def send_text_thread(page, text_field):
        try:
            text = text_field.value
            if text:
                add_message(ft.Row(
                    controls=[
                        ft.Image(src="user_avatar.jpg", width=30, height=30, border_radius=ft.border_radius.all(15)),
                        ft.Container(
                            content=ft.Text(f"Вы написали: {text}", width=200),
                            padding=10,
                            border_radius=10,
                            bgcolor="lightblue"
                        )
                    ]
                ))

                # Генерация ответа
                answer = answer_generate.generate_answer(text)
                add_message(ft.Row(
                    controls=[
                        ft.Image(src="AI_avatar.jpg", width=30, height=30, border_radius=ft.border_radius.all(15)),
                        ft.Container(
                            content=ft.Text(f"Ответ: {answer}", width=200),
                            padding=10,
                            border_radius=10,
                            bgcolor="purple"
                        )
                    ]
                ))
                text_field.value = ""
                page.update()

        except Exception as e:
            print(f"Ошибка: {e}")
            add_message(ft.Text(f"Ошибка: {e}"))

    def send_click_thread(e):
        threading.Thread(target=send_text_thread, args=(page, text_field)).start()

    def record_click_thread(e):
        threading.Thread(target=record_audio_thread, args=(page,)).start()

    # Добавляем прокручиваемый чат и другие элементы на страницу
    page.add(
        chat,
        ft.Row(
            controls=[
                text_field,
                ft.ElevatedButton("Отправить", on_click=send_click_thread),
                ft.ElevatedButton("Записать аудио", on_click=record_click_thread)
            ],
            alignment="bottom"
        ),
        recording_indicator
    )

ft.app(port=2555,target=main,view=ft.WEB_BROWSER)
