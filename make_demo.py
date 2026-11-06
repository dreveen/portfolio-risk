"""Passo 5: costruisce demo.html (una sola pagina, i dati sono dentro, il calcolo gira nel browser)."""
import json
from pathlib import Path

from returns import load_returns

HERE = Path(__file__).parent
r = load_returns()
data = {
    "tickers": list(r.columns),
    "returns": [[round(float(v), 5) for v in row] for row in r.to_numpy()],
}
html = (HERE / "demo.template.html").read_text(encoding="utf-8")
html = html.replace("__DATA__", json.dumps(data, separators=(",", ":")))
(HERE / "demo.html").write_text(html, encoding="utf-8")
print("demo.html:", round(len(html) / 1024), "KB,", len(data["returns"]), "giorni")
