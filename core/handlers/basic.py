import os
from aiogram import Bot
from aiogram.types import Message
from core.backend.audio_handler import save_voice_to_file, voice_to_text, text_to_sentence, add_emoji_to_text, open_ai_whisper
import re


async def get_text(message: Message, bot: Bot):
    """Функция для получения текстовых сообщений пользователя"""
    await message.answer("Вы прислали текстовое сообщение\! Сейчас наш бот расставит в нём смайлики\!")
    user_message = message.text
    final_result = user_message
    forward_date = message.date
    formatted_date = forward_date.strftime("%Y-%m-%d")
    formatted_time = forward_date.strftime("%H:%M:%S")
    final_result = await add_emoji_to_text(final_result)
    print(final_result)
    final_result = re.escape(final_result)
    print(final_result)
    print(f"{formatted_date} {formatted_time} | Получено аудиосообщение от {message.from_user.username} ({message.from_user.id}):\nТекст сообщения: '{final_result}'")
    await message.reply(text=f"`{final_result}`\n\n\(*нажмите на получившийся текст, чтобы его скопировать*\)")

async def get_voice(message: Message, bot:Bot):
    """Функция для получения голосовых сообщений пользователя"""
    await message.answer("Вы прислали аудиофайл\! Сейчас наш бот переведёт его в текст и расставит смайлики\!")
    print(f"{message.from_user.username} ({message.from_user.id}) отправил голосовое сообщение!")
    voice_path = await save_voice_to_file(bot, message)
    transcript_voice_text_with_google = await voice_to_text(voice_path)
    if transcript_voice_text_with_google == "error":
        await message.answer(f"*Не удалось преобразовать речь в текст*\.\n__Повторите попытку заново__\!")
        return
    transcript_voice_text_with_google = re.escape(transcript_voice_text_with_google)
    #transcript_voice_text_with_whisper = await open_ai_whisper(voice_path)
    await message.answer(f"*Google Распознавание:* {transcript_voice_text_with_google}\n\n")
    #await message.answer(f"<b>Whisper Распознавание:</b> {transcript_voice_text_with_whisper}\n\n")
    transcript_voice_text = transcript_voice_text_with_google
    forward_date = message.date
    formatted_date = forward_date.strftime("%Y-%m-%d")
    formatted_time = forward_date.strftime("%H:%M:%S")
    os.remove(voice_path + ".wav")
    os.remove(voice_path + ".ogg")
    
    if transcript_voice_text:
        # text_sentence = await text_to_sentence(transcript_voice_text)
        # text_sentence = "\n".join(transcript_voice_text)
        final_result = await add_emoji_to_text(transcript_voice_text)
        print(final_result)
        final_result = re.escape(final_result)
        print(final_result)
        await message.reply(text=f"`{final_result}`\n\n\(*нажмите на получившийся текст, чтобы его скопировать*\)")
        print(f"{formatted_date} {formatted_time} | Получено аудиосообщение от {message.from_user.username} ({message.from_user.id}):\nТекст сообщения: '{final_result}'")
