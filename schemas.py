from typing import NamedTuple


class OrderDataBybit(NamedTuple):
    avgPrice: str
    blockTradeId: str
    cancelType: str
    category: str
    closeOnTrigger: bool
    createdTime: str
    cumExecFee: str
    cumExecQty: str
    cumExecValue: str
    feeCurrency: str
    isLeverage: str
    lastPriceOnCreated: str
    leavesQty: str
    leavesValue: str
    orderId: str
    orderIv: str
    orderLinkId: str
    orderStatus: str
    orderType: str
    positionIdx: int
    price: str
    qty: str
    reduceOnly: bool
    rejectReason: str
    side: str
    slTriggerBy: str
    smpGroup: int
    smpOrderId: str
    smpType: str
    stopLoss: str
    stopOrderType: str
    symbol: str
    takeProfit: str
    timeInForce: str
    tpTriggerBy: str
    triggerBy: str
    triggerDirection: int
    triggerPrice: str
    updatedTime: str
    placeType: str = None
    # slLimitPrice: str = None


class PositionDataBybit(NamedTuple):
    bustPrice: str
    category: str
    createdTime: str
    cumRealisedPnl: str
    entryPrice: str
    leverage: str
    liqPrice: str
    markPrice: str
    positionBalance: str
    positionIdx: int
    positionMM: str
    positionIM: str
    positionStatus: str
    positionValue: str
    riskId: int
    riskLimitValue: str
    side: str
    size: str
    stopLoss: str
    symbol: str
    takeProfit: str
    tpslMode: str
    tradeMode: int
    autoAddMargin: int
    trailingStop: str
    unrealisedPnl: str
    updatedTime: str
    adlRankIndicator: int
    slLimitPrice: str = None
