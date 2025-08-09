
from __future__ import annotations
import typer
from pathlib import Path
import pandas as pd
from .connectors.sailpoint import SailPointClient
from . import certification, workflows, compliance, dashboard

app = typer.Typer(help="IAM Optimization Toolkit")

@app.command()
def fetch(out: Path = typer.Option(Path("out"), help="Output folder")):
    """Fetch (mock) data like SailPoint would (copies sample CSVs)."""
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    from shutil import copyfile
    sample = Path(__file__).resolve().parents[2] / "data" / "sample"
    for name in ["users.csv","entitlements.csv","assignments.csv","access_requests.csv","exceptions.csv"]:
        copyfile(sample / name, out / name)
    typer.echo(f"Data copied to {out}")

@app.command()
def certify(data: Path = typer.Option(Path("data/sample"), help="CSV data folder"),
            out: Path = typer.Option(Path("out/certifications"), help="Where to write decisions"),
            revoke_threshold: int = 2):
    sp = SailPointClient(data)
    users = sp.fetch_users()
    ents = sp.fetch_entitlements()
    assigns = sp.fetch_assignments()
    exc = sp.fetch_exceptions()
    camp = certification.sample_campaign(assigns, ents, n_per_risk=200)  # ~800 rows
    decisions = certification.auto_certify(camp, ents, exc, revoke_threshold=revoke_threshold)
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    decisions.to_csv(out / "decisions.csv", index=False)
    typer.echo(f"Wrote {len(decisions)} certification decisions to {out/'decisions.csv'}")

@app.command()
def doc(out: Path = typer.Option(Path("out/docs"), help="Docs folder")):
    path = workflows.render_docs(out, stats={})
    typer.echo(f"Docs written to {path}")

@app.command()
def dashboard_cmd(data: Path = typer.Option(Path("data/sample"), help="CSV data folder"),
                  decisions_csv: Path = typer.Option(Path("out/certifications/decisions.csv"), help="Decisions CSV"),
                  out: Path = typer.Option(Path("out/dashboard"), help="Dashboard output")):
    sp = SailPointClient(data)
    assigns = sp.fetch_assignments()
    ents = sp.fetch_entitlements()
    dec = pd.read_csv(decisions_csv, parse_dates=["decided_on"])
    res = dashboard.build_dashboard(assigns, ents, dec, out)
    typer.echo(f"Dashboard at {res['html']} (accuracy={res['accuracy']:.2%})")

@app.command()
def demo(out: Path = typer.Option(Path("out"), help="Root output folder")):
    fetch(out / "data")
    certify(data=Path("data/sample"), out=out / "certifications")
    doc(out / "docs")
    dashboard_cmd(data=Path("data/sample"), decisions_csv=out / "certifications" / "decisions.csv", out=out / "dashboard")

if __name__ == "__main__":
    app()
