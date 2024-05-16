import os
import requests
import soundfile as sf
from aiogram import Bot
from aiogram.types import Message
from core.settings import settings
from core.settings import Emoji
import speech_recognition as sr
import re


async def save_voice_to_file(bot: Bot, message: Message) -> str:
    """Скачивает голосовое сообщение и сохраняет в формате mp3"""
    voice = message.voice
    forward_date = message.date
    formatted_date = forward_date.strftime("%Y-%m-%d")
    formatted_time = forward_date.strftime("%H-%M-%S")

    voice_file_info = await bot.get_file(voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(settings.bots.bot_token, voice_file_info.file_path))
    voice_ogg_path = f"voice_records/{message.from_user.username}-{formatted_date}-{formatted_time}.ogg"
    voice_wav_path = f"voice_records/{message.from_user.username}-{formatted_date}-{formatted_time}.wav"
    with open(voice_ogg_path, 'wb') as f:
        f.write(file.content)
    data, samplerate = sf.read(voice_ogg_path)
    sf.write(voice_wav_path, data, samplerate)
    # os.remove(voice_ogg_path)
    voice_path = f"voice_records/{message.from_user.username}-{formatted_date}-{formatted_time}"
    return voice_path

async def voice_to_text(file_path: str) -> str:
    """Принимает путь к аудио файлу, возвращает транскрибированный текст файла."""
    r = settings.bots.google_model
    file_path = file_path + ".wav"
    voice_file = sr.AudioFile(file_path)
    result = "не удалось распознать текст"
    with voice_file as source:
        audio = r.record(source)
    try:
        result = r.recognize_google(audio, language="ru-RU")
    except Exception as e:
        print("Ошибка распознавания")
        return "error"

    # print(f"Результат распознавания: {result}")
    result = result[0].upper() + result[1:]

    sentence = await text_to_sentence(result)
    print(sentence)
    # sentenses = '. '.join(text_to_sentence(result))
    # sentenses[0].upper()
    return result

async def open_ai_whisper(filepath: str) -> str:
    text = ""
    filepath = filepath + ".ogg"
    audio_file = open(filepath, "rb")
    transcript = settings.bots.open_ai.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    print(transcript)
    return transcript.text
async def add_emoji_to_text(text: str) -> str:
    emoji_text = ""
    promo = ("Тебе на вход будет подаваться текст пользовательских сообщений."
             " Твоя задача проанализировать его и расставить после каждой смысловой части,"
             " которая может быть выделена с помощью разных пунктуационных знаком, поставить смайлики или emoji - 1 или 2 штуки,"
             " описывающий набор этих кусков текста. Смайлики должны быть интегрированы внутрь текста, с них не надо начинать предложения."
             "старайся подбирать смайлики и для существительных, но не слишком часто. Также дели выходной текст на смысловые абзацы. "
             "Не надо заменять текст смайликами - текст нужно дополнять ими. "
             "Ты можешь исправлять граматику исходного текста и раставлять знаки препинания. Смайлики должны быть разными"
             "Пусть эмодзи будут и у ключевых слов и в конце предложений. Выходной результат - это строка исходного текста с подправленной пунктуацией и грамматикой и с вставленными внутрь неё смайликами и эмодзи. Дополнять какой-то другой информацией не нужно."
             )
    chat_completion = settings.bots.open_ai.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{promo} Текст на вход: {text}"}]
    )
    emoji_text = str(chat_completion.choices[0].message.content)
    return emoji_text


async def text_to_sentence(text: str) -> [str]:
    return re.findall('[А-Я][^А-Я]*', text)


def get_sentiment_emoji(sentiment):
    """Функция соотнесения предсказанной эмоции с смайликом из словаря"""
    return Emoji.emoji_mapping.get(sentiment, "")


async def markup_text_emotional(text: str) -> str:
    """Функция для распознавания тональности сообщений и маркировки их смайликами"""
