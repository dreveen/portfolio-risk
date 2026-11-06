"""Passo 1: scarica i prezzi storici reali e li salva in data/prices.csv.

Cinque strumenti scelti per essere diversi tra loro:
azioni USA (SPY), una singola azione (AAPL), azioni europee (VGK),
obbligazioni (AGG) e oro (GLD).
"""
from pathlib import Path

import yfinance as yf

TICKERS = {
    "SPY": "Azioni USA (S&P 500)",
    "AAPL": "Apple",
    "VGK": "Azioni europee",
    "AGG": "Obbligazioni USA",
    "GLD": "Oro",
}

prices = yf.download(list(TICKERS), start="2016-01-01", end="2026-01-01",
                     auto_adjust=True, progress=False)["Close"]
prices = prices[list(TICKERS)].dropna()

out = Path(__file__).parent / "data"
out.mkdir(exist_ok=True)
prices.to_csv(out / "prices.csv")

print(f"{len(prices)} giorni di borsa, dal {prices.index[0].date()} al {prices.index[-1].date()}")
print(prices.tail(3).round(2))
