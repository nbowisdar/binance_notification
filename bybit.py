from pprint import pprint

from pybit.unified_trading import WebSocket
from time import sleep
from schemas import OrderDataBybit
from setup import notify, API_KEY_BYBIT, API_SECRET_BYBIT, TESTNET, update_message
from telebot.types import Message


ws = WebSocket(
    testnet=TESTNET,
    channel_type="private",
    api_key=API_KEY_BYBIT,
    api_secret=API_SECRET_BYBIT,
)

active_orders: dict[str, int] = {}


def build_out_message(data: OrderDataBybit):
    match data.orderStatus:
        case "New":
            order_status = "🆕 Ордер"
        case "Filled":
            order_status = "✅ Ордер заполнен"
        case "Cancelled":
            order_status = "❌ Отмена ордера"
        case "PartiallyFilled":
            order_status = "♻️ Ордер заполнен частично"
        case "Rejected":
            order_status = "❌ Ордер отклонен"
        case _:
            # order_status = "❔ Ордер"
            order_status = "✅ Ордер заполнен"

    amount_str = ""
    if float(data.cumExecValue) > 0:
        amount_str += f"Всего исполненно: <b>{data.cumExecQty}</b> {data.symbol}\n"
        amount_str += f"Сумма: <b>{data.cumExecValue}</b> USD"

    price_str = ""
    if float(data.price) > 0:
        price_str = f"Цена: {data.price} {data.symbol}"

    msg = f"""
#{data.orderType}_{data.side.upper()}
{order_status}

Кол-во: {data.qty} {data.symbol}
{price_str}
{amount_str}

    """
    return msg


def handle_order_data(message):
    print(message)
    data = OrderDataBybit(**message['data'][0])
    msg = build_out_message(data)
    print(msg)
    if data.orderStatus == "PartiallyFilled":
        msg_id = active_orders.get(data.orderId)
        msg_out = build_out_message(data)
        update_message(msg_out, msg_id)
    else:
        msg = notify(msg)
        active_orders[data.orderId] = msg.message_id

# ws.position_stream(callback=handle_message)
ws.order_stream(callback=handle_order_data)

while True:
    sleep(1)