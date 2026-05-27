import streamlit as st
import plotly.graph_objects as go

from utils.stock_data import get_stock_data
from utils.indicators import add_indicators
from utils.news_scraper import get_news

from utils.twse_name import get_stock_name

from utils.market_data import get_market_index
from utils.correlation import calculate_correlation
from utils.institutional import (
    get_real_institutional
)

from agents.sentiment_agent import analyze_sentiment
from agents.technical_agent import analyze_technical
from agents.risk_agent import analyze_risk
from agents.summary_agent import generate_summary

st.set_page_config(
    page_title="AI 股票分析系統",
    layout="wide"
)

st.title("🤖 AI 多代理股票分析平台")

stock_id = st.text_input(
    "請輸入股票代號",
    "2330"
)

if st.button("開始分析"):

    with st.spinner("AI 分析中..."):

        # 股票資料
        data = get_stock_data(stock_id)

        stock_name = get_stock_name(stock_id)

        if data.empty:
            st.error("查無股票資料")

        else:

            # 技術指標
            data = add_indicators(data)

            # 最新資料
            current_price = round(
                data["Close"].iloc[-1], 2
            )

            rsi = round(
                data["RSI"].iloc[-1], 2
            )

            ma20 = round(
                data["MA20"].iloc[-1], 2
            )

            # ===== 大盤資訊 =====

            market = get_market_index()

            st.subheader("📊 台股大盤資訊")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "加權指數",
                market["current"]
            )

            col2.metric(
                "漲跌點",
                market["change"]
            )

            col3.metric(
                "漲跌幅",
                f'{market["percent"]}%'
            )

            # ===== 股票資訊 =====

            st.subheader(
                f"📈 {stock_name} ({stock_id})"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "目前股價",
                current_price
            )

            col2.metric(
                "RSI",
                rsi
            )

            col3.metric(
                "20MA",
                ma20
            )

            # ===== K線圖 =====

            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=data.index,
                        open=data["Open"],
                        high=data["High"],
                        low=data["Low"],
                        close=data["Close"],

                        increasing_line_color="red",
                        increasing_fillcolor="red",

                        decreasing_line_color="green",
                        decreasing_fillcolor="green"
                    )
                ]
            )

            fig.update_layout(
                xaxis_rangeslider_visible=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # ===== 新聞 =====

            news = get_news(stock_id)

            st.subheader("📰 今日新聞")

            if len(news) == 0:

                st.warning("目前查無新聞")

            else:

                for item in news:

                    st.markdown(
                        f"• [{item['title']}]({item['link']})"
                    )

            # ===== 股票與大盤關聯 =====

            correlation = calculate_correlation(
                stock_id
            )

            st.subheader("📈 股票與大盤關聯")

            if correlation > 0.7:

                relation = "高度正相關"

            elif correlation > 0.4:

                relation = "中度正相關"

            else:

                relation = "低相關"

            st.write(f"相關係數：{correlation}")

            st.write(f"關聯性：{relation}")

            # ===== 三大法人 =====

            institutional = get_real_institutional(
                stock_id
            )

            if institutional is None:

                st.warning(
                    "目前查無法人資料"
                )

                institutional = {
                    "foreign": 0,
                    "investment": 0,
                    "dealer": 0
                }

            st.subheader("🏦 三大法人買賣超")

            col1, col2, col3 = st.columns(3)

            foreign_text = (
                "買超"
                if institutional["foreign"] > 0
                else "賣超"
            )

            investment_text = (
                "買超"
                if institutional["investment"] > 0
                else "賣超"
            )

            dealer_text = (
                "買超"
                if institutional["dealer"] > 0
                else "賣超"
            )

            col1.metric(
                "外資",
                f'{foreign_text} {abs(institutional["foreign"])} 張'
            )

            col2.metric(
                "投信",
                f'{investment_text} {abs(institutional["investment"])} 張'
            )

            col3.metric(
                "自營商",
                f'{dealer_text} {abs(institutional["dealer"])} 張'
            )

            # ===== Agent A =====

            st.subheader(
                "🤖 Agent A：市場情緒分析"
            )

            sentiment_result = analyze_sentiment(
                stock_id,
                news
            )

            st.info(sentiment_result)

            # ===== Agent B =====

            st.subheader(
                "🤖 Agent B：技術分析"
            )

            technical_result = analyze_technical(
                current_price,
                rsi,
                ma20
            )

            st.info(technical_result)

            # ===== Agent C =====

            st.subheader(
                "🤖 Agent C：風險分析"
            )

            risk_result = analyze_risk(
                current_price,
                rsi,
                institutional["foreign"],
                institutional["investment"],
                institutional["dealer"]
            )

            st.info(risk_result)

            # ===== Agent D =====

            st.subheader(
                "🤖 Agent D：最終投資報告"
            )

            summary_result = generate_summary(
                sentiment_result,
                technical_result,
                risk_result
            )

            st.success(summary_result)

            st.write("以上資訊僅作參考")