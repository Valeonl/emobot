from typing import Optional
from environs import Env
from dataclasses import dataclass
import speech_recognition as sr
from openai import OpenAI

@dataclass
class Bots:
    bot_token: str
    admin_id: int
    google_model: Optional[sr.Recognizer] = None
    open_ai: Optional[OpenAI] = None

@dataclass
class Emoji:
    emoji_mapping = {
        "disappointment": "😞",
        "sadness": "😢",
        "annoyance": "😠",
        "neutral": "😐",
        "disapproval": "👎",
        "realization": "😮",
        "nervousness": "😬",
        "approval": "👍",
        "happiness": "😄",
        "anger": "😡",
        "embarrassment": "😳",
        "caring": "🤗",
        "remorse": "😔",
        "disgust": "🤢",
        "grief": "😥",
        "confusion": "😕",
        "relief": "😌",
        "desire": "😍",
        "admiration": "😌",
        "optimism": "😊",
        "fear": "😨",
        "love": "❤️",
        "excitement": "🎉",
        "curiosity": "🤔",
        "amusement": "😄",
        "surprise": "😲",
        "gratitude": "🙏",
        "pride": "🦁"
    }


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID"),
            google_model=sr.Recognizer(),
            open_ai=OpenAI(api_key=env.str("OPENAI_API"), base_url=env.str("OPEN_AI_SERVICE"))

        )
    )


settings = get_settings('input')