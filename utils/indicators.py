import ta
import pandas as pd

def add_indicators(data):

    # 確保 Close 是數值型別（避免抓到字串或混入 NaN 導致指標全掛）
    if "Close" in data.columns:
        data["Close"] = pd.to_numeric(data["Close"], errors="coerce")

    # RSI
    data["RSI"] = ta.momentum.RSIIndicator(
        close=data["Close"]
    ).rsi()

    # 20MA
    data["MA20"] = (
        data["Close"]
        .rolling(window=20, min_periods=20)
        .mean()
    )

    return data