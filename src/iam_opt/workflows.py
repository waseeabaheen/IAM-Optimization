
from __future__ import annotations
from pathlib import Path
from jinja2 import Template

WORKFLOW_TMPL = Template("""
# Access Request Workflow

```mermaid
flowchart TD
    A[User submits access request] --> B{Manager approves?}
    B -- Yes --> C[Provision via IGA connector]
    B -- No --> D[Reject & notify]
    C --> E[Access granted]
    E --> F[Log evidence for audit]
```
---

# Provisioning Workflow

```mermaid
sequenceDiagram
    participant User
    participant IGA as IGA/SailPoint
    participant Target as Target System
    User->>IGA: Approved access request
    IGA->>Target: Create/Update account, assign entitlement
    Target-->>IGA: Success/Failure
    IGA-->>User: Confirmation / Exception path
```

---

# Exception Workflow

```mermaid
flowchart LR
    X[Reviewer raises exception] --> Y[Define reason + expiry]
    Y --> Z{Risk acceptable?}
    Z -- Yes --> A1[Grant temporarily]
    Z -- No --> A2[Reject exception]
    A1 --> A3[Track & re-certify before expiry]
```
""")

def render_docs(out_dir: Path, stats: dict):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    md = WORKFLOW_TMPL.render(**stats)
    (out_dir / "workflows.md").write_text(md)
    return out_dir / "workflows.md"
