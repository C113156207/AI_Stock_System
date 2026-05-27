from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

def generate_summary(
    sentiment_result,
    technical_result,
    risk_result
):

    prompt = f"""
    你是 AI 股票總分析師。

    以下是分析結果：

    【市場情緒分析】
    {sentiment_result}

    【技術分析】
    {technical_result}

    【風險分析】
    {risk_result}

    請整理成：

    1. 最終投資建議
       （強烈買入、買入、觀望、賣出）

    2. 建議原因

    3. 風險提醒

    4. 幫我用：
       🟢🟡🔴 表示建議程度

    用繁體中文回答。

    格式要像專業投資報告。
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