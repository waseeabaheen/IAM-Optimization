
from __future__ import annotations
import pandas as pd

ISO_NIST_MAP = pd.DataFrame([
    {"control":"A.9.2.3","framework":"ISO27001","requirement":"Management of privileged access"},
    {"control":"A.9.4.1","framework":"ISO27001","requirement":"Information access restriction"},
    {"control":"AC-2","framework":"NIST800-53","requirement":"Account Management"},
    {"control":"AC-6","framework":"NIST800-53","requirement":"Least Privilege"},
])

def evidence_register(decisions: pd.DataFrame, requests: pd.DataFrame) -> pd.DataFrame:
    ev = decisions.merge(requests, on=["user_id","entitlement_id"], how="left", suffixes=("","_req"))
    ev["evidence_ref"] = ev.apply(lambda r: f"REQ-{r.get('id','NA')};DEC-{str(r.name).zfill(6)}", axis=1)
    return ev

def compute_accuracy(assignments: pd.DataFrame, reconciled: pd.DataFrame) -> float:
    merged = assignments.merge(reconciled[["user_id","entitlement_id","decision"]],
                               on=["user_id","entitlement_id"], how="left")
    merged["expected_keep"] = True
    merged["is_correct"] = (merged["expected_keep"] & (merged["decision"] != "revoke")) |                            (~merged["expected_keep"] & (merged["decision"] == "revoke"))
    return float(merged["is_correct"].mean()) if len(merged) else 0.0

def control_coverage(evidence: pd.DataFrame) -> pd.DataFrame:
    cov = ISO_NIST_MAP.copy()
    cov["evidence_count"] = len(evidence)
    cov["evidence_examples"] = "; ".join(evidence["evidence_ref"].head(5).tolist())
    return cov
