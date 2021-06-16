
import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "LUJLECXFYNXKVTD0"
NEWS_API_KEY = "23b279d0b2c64cbdba68bb8856938eb3"
TWILIO_SID = "ACa18ae9347242d9fcacb58d30d149187b"
AUTH_TOKEN = "e20f683f9dc8e6d61e58d32065d10a0e"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
data = stock_response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yest_data = data_list[0]
yest_closing_price = yest_data["4. close"]
print(yest_closing_price)

day_b4_yest_data = data_list[1]
day_b4_yest_closing_price = day_b4_yest_data["4. close"]
print(day_b4_yest_closing_price)

diff = round(float(yest_closing_price) - float(day_b4_yest_closing_price), 2)
up_down = None
if diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((diff / float(yest_closing_price)) * 100, 2)
print(diff_percent)


if abs(diff_percent) > 1:
    news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[0:3]
    formatted_articles = [f"{STOCK_NAME}: {up_down} {diff_percent}%\nHeading: {article['title']}\nBrief: {article['description']}"
                          for article in three_articles]

    client = Client(TWILIO_SID, AUTH_TOKEN)

    for article in formatted_articles:
        client.messages.create(
            body=article,
            from_="+14252767491",
            to="+919836125552"
        )
