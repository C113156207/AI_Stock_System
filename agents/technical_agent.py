from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

client = OpenAI(
    api_key=st.secrets("OPENAI_API_KEY")
)

def analyze_technical(current_price, rsi, ma20):

    prompt = f"""
    你是股票技術分析師。

    目前股價：{current_price}

    RSI：{rsi}

    MA20：{ma20}

    請分析：

    1. 技術面是否偏多
    2. RSI 是否過熱
    3. 均線趨勢

    用繁體中文回答。
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content