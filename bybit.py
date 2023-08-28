from pprint import pprint
from setup import  logger
from pybit.unified_trading import WebSocket
from time import sleep
from schemas import OrderDataBybit, PositionDataBybit
from setup import notify, API_KEY_BYBIT, API_SECRET_BYBIT, TESTNET, update_message
from telebot.types import Message


ws = WebSocket(
    testnet=TESTNET,
    channel_type="private",
    api_key=API_KEY_BYBIT,
    api_secret=API_SECRET_BYBIT,
    trace_logging=True,
)

active_orders: dict[str, int] = {}


def build_out_message_position(data: PositionDataBybit):
    market = ""
    coin = data.symbol.replace("USDT", "").replace("USDC", "").replace("USD", "")
    side = "❔ symbol"
    if data.side.casefold() == "buy":
        side = "✅ symbol Long"
    elif data.side.casefold() == "sell":
        side = "⭕️ symbol Short"
    side = side.replace("symbol", f"#{data.symbol}")

    if data.markPrice:
        market = f"🧾 Цена сейчас: {data.markPrice} $"

    open_price = ""
    if data.entryPrice != "0":
        open_price = f"🌱 Вход: {data.entryPrice} $"
    take_profit = ""
    if float(data.takeProfit) > 0:
        take_profit = f"🔥 Take Profit: {data.takeProfit} $"
    stop_loss = ""
    if float(data.stopLoss) > 0:
        stop_loss = f"⛔️ Stop Loss: {data.stopLoss} $"

    cum_pnl = ""
    if float(data.cumRealisedPnl) != 0:
        cum_pnl = f"💰 Cummulative PnL: {data.cumRealisedPnl} $"
    size = ""
    if float(data.size) != 0:
        size = f"🪙 Size: {data.size} {coin}"
    if size + market + open_price + stop_loss + take_profit == "":
        return f"✅ Позиция закрыта #{data.symbol}\n{cum_pnl}"
    msg = f"""
{side}
{market}
{open_price}
{take_profit}
{stop_loss}
{cum_pnl}
Плечо: {data.leverage} 💪
{size}
""".replace("\n\n", "")
    return msg

def build_out_message_order(data: OrderDataBybit):
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
#{data.orderType.upper()}_{data.side.upper()}_{data.category.upper()}
{order_status}

Кол-во: {data.qty} {data.symbol}
{price_str}
{amount_str}

    """
    return msg

def handle_order_data_(message):
    print(message)
    data = PositionDataBybit(**message['data'][0])
    msg = build_out_message_position(data)
    msg = notify(msg)
    # active_orders[message["id"]] = msg.message_id

def handle_order_data_wallet(message):
    print(message)

def handle_order_data(message):
    try:
        data = OrderDataBybit(**message['data'][0])
    except TypeError:
        return
    msg = build_out_message_order(data)
    if data.orderStatus == "PartiallyFilled":
        msg_id = active_orders.get(data.orderId)
        msg_out = build_out_message_order(data)
        update_message(msg_out, msg_id)
    else:
        msg = notify(msg)
        active_orders[data.orderId] = msg.message_id



# ws.wallet_stream(callback=handle_order_data_wallet)

def subscribe():
    ws.position_stream(callback=handle_order_data_)
    ws.order_stream(callback=handle_order_data)


def main():
    count = 0
    global active_orders
    active_orders = {}
    subscribe()
    while count < 300:
        sleep(1)
        count += 1
#
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(e)