from pprint import pprint
from binance import ThreadedWebsocketManager
from loguru import logger
from dotenv import load_dotenv
from os import getenv
from telebot import TeleBot
import time
import messages

load_dotenv()

API_KEY = getenv("API_KEY")
API_SECRET = getenv("API_SECRET")
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
CHAT_ID = getenv("CHAT_ID")
TESTNET = getenv("TESTNET").casefold()
if TESTNET == "true":
    TESTNET = True
else:
    TESTNET = False

logger.add("logs.log", rotation="500 MB", compression="zip")
bot = TeleBot(TELEGRAM_TOKEN, parse_mode="HTML")


# last_market_orders = None
orders = {}


def build_message(data: dict) -> str | None:
    msg = None
    if data["e"] != "ORDER_TRADE_UPDATE":
        return
    logger.debug(data)
    order_data = data["o"]
    order_id = order_data["i"]
    match order_data["x"]:
        case "NEW":
            # if order_data["o"] == "MARKET":.
            orders[order_id] = order_data
            if not order_data["o"] == "MARKET":
                msg = messages.new_order(order_data)
        case "TRADE":
            if order_data["o"] == "LIMIT":
                msg = messages.limit(order_data)
            elif order_data["X"] == "FILLED":
                order = orders.get(order_id)
                if order:
                    msg = messages.market(order, order_data)
                    del orders[order_id]
        case "TAKE_PROFIT":
            msg = messages.limit(order_data)

    return msg


def handle_event(data: dict):
    msg = build_message(data)
    # msg = None
    if msg:
        bot.send_message(CHAT_ID, msg)


@logger.catch
def handling_updates():
    # client = await AsyncClient.create(api_key, api_secret)
    twm = ThreadedWebsocketManager(API_KEY, API_SECRET, testnet=TESTNET)
    # twm = ThreadedWebsocketManager(API_KEY, API_SECRET)

    twm.start()

    twm.start_futures_user_socket(handle_event)
    twm.join()


def main():
    logger.debug("Bot started")
    print(f"API Key - {API_KEY}")
    print(f"SECRET Key - {API_SECRET}")
    while True:
        handling_updates()
        logger.debug("Sleep for 60 sec")
        time.sleep(60)


if __name__ == "__main__":
    main()
