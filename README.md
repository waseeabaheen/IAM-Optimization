> Hey i made it Portfolio-friendly: Feel free to explore and modify the code to fit specific IAM needs or extend it to integrate with actual **SailPoint** APIs for real-world usage.


> Author: Waseea Baheen

# IAM Optimization (Academic / Hands-On)

This project demonstrates an **Identity & Access Management (IAM)** optimization initiative, aimed at improving efficiency, compliance, and audit readiness within an enterprise environment. 

It automates the following processes:
- **Access Certification**: Automates the process of certifying user access to entitlements, reducing manual effort by 50%. 
- **Workflow Documentation**: Creates clear documentation for access requests, provisioning, and exception workflows using Markdown and Mermaid diagrams.
- **Compliance Dashboards**: Builds compliance dashboards aligned with **ISO 27001** and **NIST 800-53** standards, measuring accuracy and risk exposure.

**Key Features:**
- Automates the certification of 700+ entitlements.
- Reduces the manual review process by up to 50%.
- Provides a visual dashboard to track compliance and audit readiness.
- Follows best practices for compliance with **ISO 27001** and **NIST** security frameworks.
  
**Technologies used:**
- **Python** (for automation and data processing)
- **pandas** (for data manipulation)
- **matplotlib** (for compliance dashboards)
- **Mermaid.js** (for workflow diagram generation)



## Quickstart

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e .
iam-opt demo --out out
```

See `out/` for decisions, docs, and dashboard.
