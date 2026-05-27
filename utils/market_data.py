import requests
import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600)
def get_market_index():

    try:

        token = st.secrets[
            "FINMIND_TOKEN"
        ]

        url = (
            "https://api.finmindtrade.com/api/v4/data"
        )

        params = {

            "dataset":
            "TaiwanStockPrice",

            # 加權指數
            "data_id": "TAIEX",

            "start_date": "2026-01-01",

            "token": token
        }

        response = requests.get(
            url,
            params=params
        )

        data = response.json()

        if "data" not in data:

            return {
                "current": 0,
                "change": 0,
                "percent": 0
            }

        df = pd.DataFrame(
            data["data"]
        )

        if df.empty:

            return {
                "current": 0,
                "change": 0,
                "percent": 0
            }

        latest = df.iloc[-1]

        current = round(
            latest["close"],
            2
        )

        change = round(
            latest["spread"],
            2
        )

        percent = round(
            latest["spread"] /
            (
                latest["close"]
                -
                latest["spread"]
            )
            * 100,
            2
        )

        return {

            "current": current,
            "change": change,
            "percent": percent
        }

    except Exception as e:

        print(e)

        return {
            "current": 0,
            "change": 0,
            "percent": 0
        }