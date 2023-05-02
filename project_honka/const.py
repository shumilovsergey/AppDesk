from dotenv import load_dotenv
import os

load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
BOT_NAME = os.getenv("BOT_NAME")
BOT_ADRES = os.getenv("BOT_ADRES")
MY_ID = os.getenv("MY_ID")
ALLOWED_HOST = os.getenv("ALLOWED_HOST")