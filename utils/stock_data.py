import yfinance as yf

def get_stock_data(stock_id):

    ticker = stock_id + ".TW"

    stock = yf.Ticker(ticker)

    data = stock.history(period="3mo")

    # yfinance 偶爾會在最新一筆出現 OHLC 全為 NaN（但 Volume 仍有值），
    # 這會導致現價/均線取最後一筆時變成 NaN。
    if not data.empty:
        ohlc_cols = ["Open", "High", "Low", "Close"]
        existing_ohlc = [c for c in ohlc_cols if c in data.columns]
        if existing_ohlc:
            data = data.dropna(subset=existing_ohlc, how="any")

    # 股票資訊
    info = stock.info

    # 中文名稱
    stock_name = (
        info.get("shortName")
        or info.get("longName")
        or "未知股票"
    )

    return data