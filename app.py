import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

FMP_KEY = os.environ.get("FMP_API_KEY", "")
FMP_BASE = "https://financialmodelingprep.com/stable"


def fmp(path, params=None):
    p = params or {}
    p["apikey"] = FMP_KEY
    r = requests.get(f"{FMP_BASE}{path}", params=p, timeout=10)
    r.raise_for_status()
    return r.json()


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/quote/<ticker>")
def quote(ticker):
    data = fmp("/quote", {"symbol": ticker.upper()})
    return jsonify(data)


@app.route("/api/profile/<ticker>")
def profile(ticker):
    data = fmp("/profile", {"symbol": ticker.upper()})
    return jsonify(data)


@app.route("/api/ratios/<ticker>")
def ratios(ticker):
    data = fmp("/ratios-ttm", {"symbol": ticker.upper()})
    return jsonify(data)


@app.route("/api/income/<ticker>")
def income(ticker):
    data = fmp("/income-statement", {"symbol": ticker.upper(), "limit": 4})
    return jsonify(data)


@app.route("/api/balance/<ticker>")
def balance(ticker):
    data = fmp("/balance-sheet-statement", {"symbol": ticker.upper(), "limit": 4})
    return jsonify(data)


@app.route("/api/cashflow/<ticker>")
def cashflow(ticker):
    data = fmp("/cash-flow-statement", {"symbol": ticker.upper(), "limit": 4})
    return jsonify(data)


@app.route("/api/peers/<ticker>")
def peers(ticker):
    data = fmp("/stock-peers", {"symbol": ticker.upper()})
    return jsonify(data)


@app.route("/api/history/<ticker>")
def history(ticker):
    data = fmp("/historical-price-eod/full", {"symbol": ticker.upper(), "serietype": "line", "timeseries": 252})
    return jsonify(data)


@app.route("/api/dcf/<ticker>")
def dcf(ticker):
    data = fmp("/discounted-cash-flow", {"symbol": ticker.upper()})
    return jsonify(data)


@app.route("/api/analyst/<ticker>")
def analyst(ticker):
    data = fmp("/analyst-stock-recommendations", {"symbol": ticker.upper(), "limit": 5})
    return jsonify(data)


@app.route("/api/earnings/<ticker>")
def earnings(ticker):
    data = fmp("/earning-calendar", {"symbol": ticker.upper(), "limit": 8})
    return jsonify(data)


@app.route("/api/news/<ticker>")
def news(ticker):
    data = fmp("/news/stock", {"symbol": ticker.upper(), "limit": 8})
    return jsonify(data)


@app.route("/api/keydmetrics/<ticker>")
def key_metrics(ticker):
    data = fmp("/key-metrics-ttm", {"symbol": ticker.upper()})
    return jsonify(data)


@app.route("/api/ma/<ticker>")
def ma_search(ticker):
    data = fmp("/mergers-acquisitions-rss-feed", {"page": 0})
    return jsonify(data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
