> Hey i made it Portfolio-friendly: if you wanna use it just swap the mock connector with real SailPoint APIs. :)
> 
# IAM Optimization (Academic / Hands-On)
A reproducible Python project that simulates an IAM optimization initiative:
- **Automated access certification** for 700+ entitlements (SailPoint-style connector).
- **Workflow documentation**: access request, provisioning, and exceptions (Markdown + Mermaid).
- **Compliance dashboard** with accuracy metrics aligned to **ISO/IEC 27001** and **NIST 800-53** mappings.



## Quickstart

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e .
iam-opt demo --out out
```

See `out/` for decisions, docs, and dashboard.
