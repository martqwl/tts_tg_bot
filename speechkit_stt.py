import requests
from config_stt import IAM_TOKEN, FOLDER_ID, params, headers, URL
import requests
def speech_to_text(data):
    # Выполняем запрос
    response = requests.post(
        f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}",
        headers=headers,
        data=data
    )

    # Читаем json в словарь
    decoded_data = response.json()
    # Проверяем, не произошла ли ошибка при запросе
    if decoded_data.get("error_code") is None:
        return True, decoded_data.get("result")  # Возвращаем статус и текст из аудио
    else:
        return False, "При запросе в SpeechKit возникла ошибка"

    return True, decoded_data['result']

def text_to_speech(text: str):
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
    }
    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': 'marina',
        'emotion': 'whisper',
        'folderId': FOLDER_ID,
    }
    response = requests.post(URL, headers=headers, data=data)
    if response.status_code == 200:
        return True, response.content
    else:
        return False, f"При запросе в SpeechKit возникла ошибка {response.status_code}"
