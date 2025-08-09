
from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from datetime import datetime

Risk = Literal["low", "medium", "high", "critical"]

class Entitlement(BaseModel):
    id: str
    system: str
    name: str
    description: Optional[str] = None
    owner: Optional[str] = None
    risk: Risk = "medium"

class User(BaseModel):
    id: str
    display_name: str
    department: str
    manager_id: Optional[str] = None
    status: Literal["active", "inactive"] = "active"

class Assignment(BaseModel):
    user_id: str
    entitlement_id: str
    granted_on: datetime
    source: Literal["request", "provisioning", "exception"] = "request"

class AccessRequest(BaseModel):
    id: str
    user_id: str
    entitlement_id: str
    justification: Optional[str] = None
    created_on: datetime
    approved_by: Optional[str] = None
    status: Literal["approved","rejected","pending"] = "approved"

class ExceptionRecord(BaseModel):
    id: str
    user_id: str
    entitlement_id: str
    reason: str
    expires_on: Optional[datetime]

class CertificationDecision(BaseModel):
    user_id: str
    entitlement_id: str
    decision: Literal["keep","revoke","escalate"]
    reviewer: str
    rationale: str
    decided_on: datetime

class ControlMapping(BaseModel):
    control: str
    framework: Literal["ISO27001", "NIST800-53"]
    requirement: str
    evidence: List[str] = Field(default_factory=list)
