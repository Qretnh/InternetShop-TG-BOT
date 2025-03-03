import requests
from environs import Env

env = Env()
env.read_env()


def send(user_id: int,
         message: str,
         buttons: list[str:str] = None):
    BOT_TOKEN = env("BOT_TOKEN")
    CHAT_ID = user_id
    message_text = message

    keyboard = [
        [{"text": button[0], "url": button[1]}] for button in buttons
    ] if buttons else None

    inline_keyboard = {
        "inline_keyboard": keyboard
    }

    # URL для отправки сообщения
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    if buttons:
        payload = {
            "chat_id": CHAT_ID,
            "text": message_text,
            "reply_markup": inline_keyboard
        }
    else:
        payload = {
            "chat_id": CHAT_ID,
            "text": message_text,
        }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Сообщение успешно отправлено!")
        return 1
    else:
        print(f"Ошибка: {response.status_code}, {response.text}")
        return 0
