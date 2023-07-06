def get_smile(type_trade: str) -> str:
    if type_trade == "LONG":
        smile = "✅"
    elif type_trade == "SHORT":
        smile = "⭕️"
    else:
        smile = "❔"
    return smile


triggers = ["TAKE_PROFIT_MARKET", "STOP_MARKET"]


def new_order(d: dict) -> str:
    stop_price = float(d["sp"])
    if d["o"].upper() in triggers:
        coin = d["s"].replace(d["N"], "")
        price = f"Цена: {d['p']} {d['N']}"
        stop = ""
        if stop_price:
            stop = f"Trigger Price: {d['sp']} {d['N']}"
        if d["o"].casefold() == "market":
            price = ""

        return f"""
    🆕 Новый ордер
    #{d['s']}
    #{d['o']}_{d['S']}

    Кол-во: {d['q']} {coin}
    {price}
    {stop}
    """
    t = d["o"]
    stop = f"Trigger Price: {d['sp']} {d['N']}"
    return f"""
{t}
{stop}
"""


def market(o, d: dict) -> str:
    type_trade = d["ps"].upper()
    pos = "Position"
    if type_trade != "BOTH":
        pos = type_trade

    coin = d["s"].replace(d["N"], "")
    # proc = round(float(d["z"]) * 100)
    s = round(float(d["ap"]) * float(d["z"]))
    avg_price = round(float(d["ap"]))
    profit = ""
    changed_balance = float(d["rp"])

    smile = get_smile(type_trade)
    open_close = "OPEN"

    if changed_balance:
        open_close = "CLOSE"
        profit = f"Profit {round(changed_balance, 2)} {d['N']}"
    return f"""
{smile} #{d['s']}
#{d['o']}_{o['S']}
{pos} {open_close} 

Кол-во: {d["z"]} {coin}
Средняя цена:  {avg_price} {d['N']}
Сумма:  {s} {d['N']}

{profit}
"""


def limit(d: dict) -> str:
    type_trade = d["ps"].upper()
    pos = "Position"
    if type_trade != "BOTH":
        pos = type_trade
    if d["S"] == "SELL":
        buy_sell = "продано"
    else:
        buy_sell = "куплено"

    coin = d["s"].replace(d["N"], "")
    symbol_stable = d["s"]
    stable_coin = d["N"]
    type_deal = d["o"]

    changed_balance = float(d["rp"])

    open_close = "OPEN"
    profit = ""
    smile = get_smile(type_trade)
    if changed_balance:
        open_close = "CLOSE"
        profit = f"Profit {round(changed_balance, 2)} {d['N']}"
    s = round(float(d["p"]) * float(d["l"]))
    return f"""
{smile} #{symbol_stable}
#{type_deal}_{d['S']}
{pos} {open_close} 

Кол-во: {d["l"]} {coin}
Цена: {d['p']} {stable_coin}
Сумма:  {s} {stable_coin}

Всего {buy_sell} {d['z']} {coin}

{profit}
"""


def take_profit(d: dict) -> str:
    if d["S"] == "SELL":
        buy_sell = "продано"
    else:
        buy_sell = "куплено"

    coin = d["s"].replace(d["N"], "")
    symbol_stable = d["s"]
    stable_coin = d["N"]
    type_deal = d["o"]
    s = round(float(d["p"]) * float(d["l"]))

    type_trade = d["ps"].upper()

    smile = get_smile(type_trade)

    return f"""
{smile} #{symbol_stable}
#{type_deal}_{d['S']}

Кол-во: {d["l"]} {coin}
Цена: {d['p']} {stable_coin}
Сумма:  {s} {stable_coin}

Всего {buy_sell} {d['z']} {coin}
"""
