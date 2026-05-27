import yfinance as yf

def calculate_correlation(stock_id):

    stock = yf.Ticker(stock_id + ".TW")

    market = yf.Ticker("^TWII")

    stock_data = stock.history(period="3mo")

    market_data = market.history(period="3mo")

    stock_close = stock_data["Close"]

    market_close = market_data["Close"]

    correlation = stock_close.corr(
        market_close
    )

    return round(correlation, 2)