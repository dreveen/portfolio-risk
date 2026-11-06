"""Passo 4: il grafico dei futuri simulati e della perdita nel 5% dei casi peggiori (italiano e inglese)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from simulate import START, simulate, summarize

GREEN, RED, TEXT, MUTED, BG = "#3ddc97", "#ff5c6c", "#e8eef5", "#8a98a8", "#0e1621"

LABELS = {
    "it": {"file": "risultati.png", "sep": ".", "left": "10.000 futuri possibili in un anno", "median": "Caso mediano",
           "worst": "5% peggiore", "x": "Giorni di borsa", "y": "Valore del portafoglio (€)",
           "right": "Dove finiscono i tuoi soldi", "xr": "Valore dopo un anno (€)",
           "note": "In 19 casi su 20\nnon perdi più\ndi {v} €"},
    "en": {"file": "results_en.png", "sep": ",", "left": "10,000 possible futures in one year", "median": "Median case",
           "worst": "Worst 5%", "x": "Trading days", "y": "Portfolio value (€)",
           "right": "Where your money ends up", "xr": "Value after one year (€)",
           "note": "In 19 of 20 cases\nyou lose no\nmore than {v} €"},
}

paths = simulate()
final = paths[:, -1]
stats = summarize(paths)
p5 = np.percentile(final, 5)
x = np.arange(paths.shape[1])
var95 = stats["perdita nel 5% dei casi peggiori (VaR 95%)"]


def draw(lang):
    t = LABELS[lang]
    plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": TEXT,
                         "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
    fig, (a, b) = plt.subplots(1, 2, figsize=(13, 5.2), gridspec_kw={"width_ratios": [1.5, 1]})
    fig.patch.set_facecolor(BG)
    for ax in (a, b):
        ax.set_facecolor(BG)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color("#2a3646")

    # sinistra: 150 futuri a caso + fasce dei percentili
    for p in paths[:150]:
        a.plot(x, p, color=GREEN, alpha=0.07, lw=0.8)
    lo, med, hi = (np.percentile(paths, q, axis=0) for q in (5, 50, 95))
    a.fill_between(x, lo, hi, color=GREEN, alpha=0.12, lw=0)
    a.plot(x, med, color=GREEN, lw=2.2, label=t["median"])
    a.plot(x, lo, color=RED, lw=1.6, ls="--", label=t["worst"])
    a.axhline(START, color=MUTED, lw=0.8, ls=":")
    a.set_xlabel(t["x"])
    a.set_ylabel(t["y"])
    a.set_title(t["left"], loc="left", color=TEXT, fontsize=13, pad=12)
    a.legend(frameon=False, labelcolor=TEXT, loc="upper left")

    # destra: distribuzione dei valori finali, 5% peggiore in rosso
    bins = np.linspace(final.min(), np.percentile(final, 99.5), 60)
    n, edges, patches = b.hist(final, bins=bins, color=GREEN, alpha=0.75)
    for left, patch in zip(edges[:-1], patches):
        if left < p5:
            patch.set_facecolor(RED)
    b.axvline(START, color=MUTED, lw=0.8, ls=":")
    b.set_xlabel(t["xr"])
    b.set_yticks([])
    b.set_title(t["right"], loc="left", color=TEXT, fontsize=13, pad=12)
    b.annotate(t["note"].format(v=f"{var95:,.0f}".replace(",", t["sep"])),
               xy=(p5 - 350, n.max() * 0.17), xytext=(edges[0], n.max() * 0.62),
               color=TEXT, fontsize=10.5, ha="left", arrowprops=dict(arrowstyle="->", color=RED, lw=1.3))

    fig.tight_layout(pad=2)
    out = Path(__file__).parent / "docs"
    out.mkdir(exist_ok=True)
    fig.savefig(out / t["file"], dpi=150, facecolor=BG)
    plt.close(fig)
    print("salvato", out / t["file"])


for lang in LABELS:
    draw(lang)
