
from __future__ import annotations
import pandas as pd
from pathlib import Path

class SailPointClient:
    """Mock SailPoint data fetcher. Replace methods with real API calls in production."""
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)

    def fetch_users(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "users.csv")

    def fetch_entitlements(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "entitlements.csv")

    def fetch_assignments(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "assignments.csv", parse_dates=["granted_on"])

    def fetch_access_requests(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "access_requests.csv", parse_dates=["created_on"])

    def fetch_exceptions(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "exceptions.csv", parse_dates=["expires_on"])
