from binance import ThreadedWebsocketManager
from loguru import logger
from dotenv import load_dotenv
from os import getenv
from telebot import TeleBot
import time

load_dotenv()

API_KEY = getenv("API_KEY")
API_SECRET = getenv("API_SECRET")
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
CHAT_ID = getenv("CHAT_ID")

logger.add("logs.log", rotation="500 MB", compression="zip")
bot = TeleBot(TELEGRAM_TOKEN, parse_mode="HTML")


ignore_events = ["WITHDRAW", "DEPOSIT"]


def build_message(data: dict) -> str:
    # TODO build right message
    resp = ""
    ud: str = data["a"]

    if ud["m"].upper() in ignore_events:
        logger.debug("Ignore event")
        return

    resp += f"Operation: {ud['m']}\n"

    if ud["B"]:
        for items in ud["B"]:
            for k, v in items.items():
                resp += f"{k}: {v}\n"

    if ud["P"]:
        for items in ud["P"]:
            for k, v in items.items():
                resp += f"{k}: {v}\n"

    return resp


def handle_event(data: dict):
    logger.debug(data)
    msg = build_message(data)
    if msg:
        bot.send_message(CHAT_ID, msg)


@logger.catch
def handling_updates():
    # client = await AsyncClient.create(api_key, api_secret)
    twm = ThreadedWebsocketManager(API_KEY, API_SECRET)

    twm.start()

    twm.start_futures_user_socket(handle_event)
    twm.join()


def main():
    bot.send_message(CHAT_ID, "Bot started")
    while True:
        handling_updates()
        logger.debug("Sleep for 60 sec")
        time.sleep(60)


if __name__ == "__main__":
    main()
