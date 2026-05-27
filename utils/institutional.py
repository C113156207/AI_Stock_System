import requests
import pandas as pd

def get_real_institutional(stock_id):

    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiTGluemVFbHplIiwiZW1haWwiOiJtYW9pbGVnY2F0QGdtYWlsLmNvbSIsInRva2VuX3ZlcnNpb24iOjB9.YSWmwwtLtLwRwGrhCgQQajQ-1qFfJYmLhQVDdktb44M"

    url = (
        "https://api.finmindtrade.com/api/v4/data"
    )

    headers = {
        "Authorization":
        f"Bearer {token}"
    }

    params = {

        "dataset":
        "TaiwanStockInstitutionalInvestorsBuySell",

        "data_id": stock_id,

        # 不要用今天
        "start_date": "2025-01-01"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    data = response.json()

    if "data" not in data:

        return None

    df = pd.DataFrame(data["data"])

    if df.empty:

        return None

    # ===== 抓最近有資料的一天 =====

    latest_date = df["date"].max()

    latest_df = df[
        df["date"] == latest_date
    ]

    result = {
        "foreign": 0,
        "investment": 0,
        "dealer": 0
    }

    for _, row in latest_df.iterrows():

        name = row["name"]

        # FinMind 沒有 buy_sell
        buy = row["buy"]
        sell = row["sell"]

        buy_sell = buy - sell

        if name == "Foreign_Investor":

            result["foreign"] = buy_sell

        elif name == "Investment_Trust":

            result["investment"] = buy_sell

        elif (
            name == "Dealer_self"
            or
            name == "Dealer_Hedging"
        ):

            result["dealer"] += buy_sell

    return result