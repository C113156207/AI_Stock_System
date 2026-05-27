from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

client = OpenAI(
    api_key=st.secrets("OPENAI_API_KEY")
)

def analyze_risk(
    current_price,
    rsi,
    foreign,
    investment,
    dealer
):

    prompt = f"""
    你是股票風險控管專家。

    目前股價：{current_price}

    RSI：{rsi}

    外資：
    {foreign}

    投信：
    {investment}

    自營商：
    {dealer}

    請分析：

    1. 目前風險程度
    2. 法人是偏多還偏空
    3. 是否適合進場
    4. 停損建議

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