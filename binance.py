from pprint import pprint
from binance import ThreadedWebsocketManager
import time
import messages
from setup import notify, logger
import setup


def handle_event(data: dict):
    msg = build_message(data)
    if msg:
        notify(msg)


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



@logger.catch
def handling_updates():
    # client = await AsyncClient.create(setup.API_KEY_BINANCE, setup.API_SECRET_BINANCE,)

    twm = ThreadedWebsocketManager(setup.API_KEY_BINANCE, setup.API_SECRET_BINANCE, testnet=setup.TESTNET)
    # twm = ThreadedWebsocketManager(setup.API_KEY_BINANCE, setup.API_SECRET_BINANCE,)

    twm.start()
    twm.start_futures_user_socket(handle_event)
    twm.join()


def main():
    logger.debug("Bot started")
    print(f"API Key - {setup.API_KEY_BINANCE}")
    print(f"SECRET Key - {setup.API_SECRET_BINANCE}")
    while True:
        handling_updates()
        logger.debug("Sleep for 60 sec")
        time.sleep(60)


if __name__ == "__main__":
    main()
