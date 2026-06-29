import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

FMP_KEY = os.environ.get("FMP_API_KEY", "")
FMP_BASE = "https://financialmodelingprep.com/api/v3"
FMP_STABLE = "https://financialmodelingprep.com/stable"


def fmp(path, params=None, stable=False):
    base = FMP_STABLE if stable else FMP_BASE
    p = params or {}
    p["apikey"] = FMP_KEY
    r = requests.get(f"{base}{path}", params=p, timeout=10)
    r.raise_for_status()
    return r.json()


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/quote/<ticker>")
def quote(ticker):
    data = fmp(f"/quote/{ticker.upper()}")
    return jsonify(data)


@app.route("/api/profile/<ticker>")
def profile(ticker):
    data = fmp(f"/profile/{ticker.upper()}")
    return jsonify(data)


@app.route("/api/ratios/<ticker>")
def ratios(ticker):
    data = fmp(f"/ratios-ttm/{ticker.upper()}")
    return jsonify(data)


@app.route("/api/income/<ticker>")
def income(ticker):
    data = fmp(f"/income-statement/{ticker.upper()}", {"limit": 4})
    return jsonify(data)


@app.route("/api/balance/<ticker>")
def balance(ticker):
    data = fmp(f"/balance-sheet-statement/{ticker.upper()}", {"limit": 4})
    return jsonify(data)


@app.route("/api/cashflow/<ticker>")
def cashflow(ticker):
    data = fmp(f"/cash-flow-statement/{ticker.upper()}", {"limit": 4})
    return jsonify(data)


@app.route("/api/peers/<ticker>")
def peers(ticker):
    data = fmp(f"/stock_peers", {"symbol": ticker.upper()})
    return jsonify(data)


@app.route("/api/history/<ticker>")
def history(ticker):
    data = fmp(f"/historical-price-full/{ticker.upper()}", {"serietype": "line", "timeseries": 252})
    return jsonify(data)


@app.route("/api/dcf/<ticker>")
def dcf(ticker):
    data = fmp(f"/discounted-cash-flow/{ticker.upper()}")
    return jsonify(data)


@app.route("/api/analyst/<ticker>")
def analyst(ticker):
    data = fmp(f"/analyst-stock-recommendations/{ticker.upper()}", {"limit": 5})
    return jsonify(data)


@app.route("/api/earnings/<ticker>")
def earnings(ticker):
    data = fmp(f"/historical/earning_calendar/{ticker.upper()}", {"limit": 8})
    return jsonify(data)


@app.route("/api/news/<ticker>")
def news(ticker):
    data = fmp(f"/stock_news", {"tickers": ticker.upper(), "limit": 8})
    return jsonify(data)


@app.route("/api/keydmetrics/<ticker>")
def key_metrics(ticker):
    data = fmp(f"/key-metrics-ttm/{ticker.upper()}")
    return jsonify(data)


@app.route("/api/ma/<ticker>")
def ma_search(ticker):
    data = fmp(f"/mergers-acquisitions-rss-feed", {"page": 0}, stable=True)
    return jsonify(data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
