from dotenv import load_dotenv
from os import getenv
from telebot import TeleBot
from loguru import logger
from telebot.types import Message

load_dotenv()

# Binance
API_KEY_BINANCE = getenv("API_KEY_BINANCE")
API_SECRET_BINANCE = getenv("API_SECRET_BINANCE")

# Bybit
API_KEY_BYBIT = getenv("API_KEY_BYBIT")
API_SECRET_BYBIT = getenv("API_SECRET_BYBIT")

TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
CHAT_ID = getenv("CHAT_ID")
TESTNET = getenv("TESTNET").casefold()

if TESTNET == "true":
    TESTNET = True
else:
    TESTNET = False

logger.add("logs.log", rotation="500 MB", compression="zip")

bot = TeleBot(TELEGRAM_TOKEN, parse_mode="HTML")


def notify(msg: str) -> Message:
    return bot.send_message(CHAT_ID, msg)


def update_message(msg_out: str, message_id: int):
    bot.edit_message_text(
        chat_id=CHAT_ID,
        message_id=message_id,
        text=msg_out,
        parse_mode="HTML")