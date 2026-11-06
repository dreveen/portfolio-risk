"""Passo 2: dai prezzi ai rendimenti giornalieri, volatilita' e correlazioni.

Il rendimento di un giorno e' quanto e' variato il prezzo rispetto al giorno prima
(es. +1,2%). La simulazione useremo questi numeri come "carattere" di ogni strumento.
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent


def load_returns():
    prices = pd.read_csv(HERE / "data" / "prices.csv", index_col=0, parse_dates=True)
    return prices.pct_change().dropna()


if __name__ == "__main__":
    r = load_returns()
    days = 252  # giorni di borsa in un anno

    summary = pd.DataFrame({
        "rendimento medio annuo %": r.mean() * days * 100,
        "volatilita' annua %": r.std() * np.sqrt(days) * 100,
        "peggior giorno %": r.min() * 100,
        "miglior giorno %": r.max() * 100,
    }).round(1)
    print(summary.to_string())
    print("\nCorrelazioni (1 = si muovono insieme, 0 = indipendenti, negativo = opposti):")
    print(r.corr().round(2).to_string())
