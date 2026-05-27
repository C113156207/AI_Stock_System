from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

client = OpenAI(
    api_key=st.secrets("OPENAI_API_KEY")
)

def analyze_sentiment(stock_id, news):

    prompt = f"""
    你是股票市場輿情分析師。

    股票代號：{stock_id}

    新聞：
    {news}

    請分析：

    1. 市場情緒
    2. 情緒分數（1~5）
    3. 是否偏多或偏空

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