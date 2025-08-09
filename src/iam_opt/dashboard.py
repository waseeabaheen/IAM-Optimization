
from __future__ import annotations
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def _save_bar(series: pd.Series, title: str, out: Path, filename: str):
    out.mkdir(parents=True, exist_ok=True)
    plt.figure()
    series.plot(kind="bar")
    plt.title(title)
    plt.tight_layout()
    p = out / filename
    plt.savefig(p)
    plt.close()
    return p

def build_dashboard(assignments: pd.DataFrame,
                    entitlements: pd.DataFrame,
                    decisions: pd.DataFrame,
                    out_dir: Path) -> dict:
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    decision_counts = decisions["decision"].value_counts()
    p1 = _save_bar(decision_counts, "Certification Decisions", out, "decisions.png")

    risk_weight = {"low":1,"medium":2,"high":3,"critical":4}
    dec = decisions.merge(entitlements[["id","system","risk"]], left_on="entitlement_id", right_on="id", how="left")
    kept = dec[dec["decision"]!="revoke"]
    exposure = kept.groupby("system")["risk"].apply(lambda s: sum(risk_weight.get(x,2) for x in s))
    p2 = _save_bar(exposure, "Risk Exposure (Kept) by System", out, "exposure.png")

    accuracy = (decisions["decision"]!="revoke").mean()
    (out / "metrics.json").write_text(pd.Series({"accuracy": float(accuracy)}).to_json())

    html = f"""
    <html><head><meta charset="utf-8"><title>IAM Dashboard</title></head>
    <body>
    <h1>IAM Compliance Dashboard</h1>
    <p><strong>Reconciliation accuracy (proxy):</strong> {accuracy:.2%}</p>
    <img src="decisions.png" alt="decisions" width="640"/>
    <img src="exposure.png" alt="exposure" width="640"/>
    </body></html>
    """
    (out / "index.html").write_text(html)
    return {"accuracy": float(accuracy), "html": str(out / "index.html"), "images": [str(p1), str(p2)]}
