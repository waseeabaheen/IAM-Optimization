
from __future__ import annotations
import pandas as pd

def risk_score(row: pd.Series) -> int:
    risk_map = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    base = risk_map.get(str(row.get("risk", "medium")).lower(), 2)
    recency_bonus = 1 if (pd.Timestamp.now() - pd.to_datetime(row.get("granted_on"))).days < 30 else 0
    exception_bonus = 1 if bool(row.get("is_exception", False)) else 0
    return int(base + recency_bonus + exception_bonus)

def auto_certify(
    assignments: pd.DataFrame,
    entitlements: pd.DataFrame,
    exceptions: pd.DataFrame,
    reviewer: str = "auto-reviewer@org",
    revoke_threshold: int = 2
) -> pd.DataFrame:
    """
    Simple automated access certification:

    - Risk scoring combines entitlement risk, recency, and exception flag.
    - Keep if score <= revoke_threshold, else revoke.
    - Escalate when risk is 'critical' and assignment is an active exception.
    Returns a DataFrame of decisions.
    """
    ex_keys = set(zip(exceptions.get("user_id", []), exceptions.get("entitlement_id", []))) if exceptions is not None and not exceptions.empty else set()

    df = assignments.merge(
        entitlements[["id", "risk"]],
        left_on="entitlement_id",
        right_on="id",
        how="left"
    )
    # vectorized exception flag
    df["is_exception"] = df.apply(lambda r: (r["user_id"], r["entitlement_id"]) in ex_keys, axis=1)
    df["score"] = df.apply(risk_score, axis=1)

    decisions = []
    now = pd.Timestamp.now()
    for _, r in df.iterrows():
        decision = "keep" if r["score"] <= revoke_threshold else "revoke"
        if str(r.get("risk", "medium")).lower() == "critical" and r["is_exception"]:
            decision = "escalate"
        rationale = f"score={r['score']} risk={r.get('risk','?')} exception={bool(r['is_exception'])}"
        decisions.append({
            "user_id": r["user_id"],
            "entitlement_id": r["entitlement_id"],
            "decision": decision,
            "reviewer": reviewer,
            "rationale": rationale,
            "decided_on": now
        })
    return pd.DataFrame(decisions)

def sample_campaign(assignments: pd.DataFrame, entitlements: pd.DataFrame, n_per_risk: int = 50) -> pd.DataFrame:
    """Build a campaign of ~700+ entitlements by sampling per risk tier."""
    out = []
    for risk in ["critical", "high", "medium", "low"]:
        eids = entitlements.query("risk == @risk")["id"]
        samp = assignments[assignments["entitlement_id"].isin(eids)]
        if len(samp) > n_per_risk:
            samp = samp.sample(n_per_risk, random_state=7)
        out.append(samp)
    return pd.concat(out, ignore_index=True)
