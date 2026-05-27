import yfinance as yf

def get_market_index():

    twii = yf.Ticker("^TWII")

    data = twii.history(period="5d")

    current = round(data["Close"].iloc[-1], 2)

    previous = round(data["Close"].iloc[-2], 2)

    change = round(current - previous, 2)

    percent = round((change / previous) * 100, 2)

    return {
        "current": current,
        "change": change,
        "percent": percent
    }