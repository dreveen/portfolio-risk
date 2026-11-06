"""Passo 3: simulazione Monte Carlo di un anno di investimento.

Metodo (bootstrap storico): per ogni futuro simulato si pescano a caso 252 giorni
dalla storia, con rimpiazzo, e si applicano i rendimenti di quei giorni al portafoglio.
Si pesca l'intera riga di un giorno (tutti e 5 gli strumenti insieme), quindi le
correlazioni e i giorni di crollo reali restano intatti.
"""
import numpy as np

from returns import load_returns

DAYS = 252
START = 10_000  # euro investiti
WEIGHTS = {"SPY": 0.40, "AAPL": 0.10, "VGK": 0.10, "AGG": 0.30, "GLD": 0.10}


def simulate(weights=WEIGHTS, n_sims=10_000, horizon=DAYS, start=START, seed=42):
    """Restituisce una matrice (n_sims, horizon + 1) con il valore del portafoglio giorno per giorno."""
    r = load_returns()
    w = np.array([weights[c] for c in r.columns])
    assert abs(w.sum() - 1) < 1e-9, "i pesi devono sommare a 1"

    rng = np.random.default_rng(seed)
    picks = rng.integers(0, len(r), size=(n_sims, horizon))  # giorni storici pescati
    daily = r.to_numpy()[picks] @ w                           # rendimento del portafoglio ogni giorno
    paths = start * np.cumprod(1 + daily, axis=1)
    return np.hstack([np.full((n_sims, 1), float(start)), paths])


def summarize(paths, start=START):
    final = paths[:, -1]
    var95 = start - np.percentile(final, 5)          # perdita superata solo nel 5% dei casi
    tail = final[final <= np.percentile(final, 5)]   # il 5% dei casi peggiori
    return {
        "valore finale mediano": np.median(final),
        "perdita nel 5% dei casi peggiori (VaR 95%)": var95,
        "perdita media nel 5% peggiore (CVaR)": start - tail.mean(),
        "probabilita' di chiudere in perdita %": (final < start).mean() * 100,
    }


if __name__ == "__main__":
    paths = simulate()
    print(f"{len(paths):,} futuri simulati di {paths.shape[1] - 1} giorni, partendo da {START:,} euro\n")
    for k, v in summarize(paths).items():
        print(f"{k}: {v:,.1f}")
