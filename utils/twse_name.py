import requests
import pandas as pd
from io import StringIO

def get_stock_name(stock_id):

    url = (
        "https://isin.twse.com.tw/isin/"
        "C_public.jsp?strMode=2"
    )

    response = requests.get(url)

    response.encoding = "big5"

    tables = pd.read_html(
        StringIO(response.text)
    )

    df = tables[0]

    df.columns = df.iloc[0]

    df = df[1:]

    for _, row in df.iterrows():

        stock_info = str(
            row["有價證券代號及名稱"]
        )

        try:

            parts = stock_info.split("　")

            code = parts[0]

            name = parts[1]

            # 精確比對
            if code == stock_id:

                return name

        except:
            pass

    return "未知股票"