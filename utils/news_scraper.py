import feedparser

def get_news(stock_id):

    rss_url = f"https://tw.stock.yahoo.com/rss?s={stock_id}"

    feed = feedparser.parse(rss_url)

    news_list = []

    for entry in feed.entries[:5]:

        news_list.append({
            "title": entry.title,
            "link": entry.link
        })

    return news_list