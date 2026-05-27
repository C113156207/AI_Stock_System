import requests
import pandas as pd
import streamlit as st
import os

@st.cache_data(ttl=3600)
def get_stock_data(stock_id):

    try:

        token = st.secrets[
            "FINMIND_TOKEN"
        ]

        url = (
            "https://api.finmindtrade.com/api/v4/data"
        )

        params = {
            "dataset": "TaiwanStockPrice",
            "data_id": stock_id,
            "start_date": "2026-01-01",
            "token": token
        }

        response = requests.get(
            url,
            params=params
        )

        data = response.json()

        if "data" not in data:

            return None

        df = pd.DataFrame(data["data"])

        if df.empty:

            return None

        # 日期轉換
        df["date"] = pd.to_datetime(
            df["date"]
        )

        df.set_index(
            "date",
            inplace=True
        )

        # 改成 yfinance 格式
        df.rename(columns={

            "open": "Open",
            "max": "High",
            "min": "Low",
            "close": "Close",
            "Trading_Volume": "Volume"

        }, inplace=True)

        return df

    except Exception as e:

        print(e)

        return None