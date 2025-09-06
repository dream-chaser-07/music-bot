import os

class Config:
    API_ID = int(os.getenv("API_ID", 0))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    ADMINS = [int(x) for x in os.getenv("ADMINS", "0").split()]
    SESSION_NAME = os.getenv("SESSION_NAME", "MusicBot")
