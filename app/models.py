from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal
from datetime import datetime

class Payment(BaseModel):
    payment_id: str = Field(min_length=1)
    amount: float = Field(ge=0)
    currency: str
    status: str
    method: str
    created_at: datetime

class Dispute(BaseModel):
    dispute_id: str
    reason: str
    customer_claim: str
    created_at: datetime

class MerchantEvidence(BaseModel):
    order_id: Optional[str] = None
    product_description: Optional[str] = None
    delivery_status: Optional[str] = None
    delivery_date: Optional[datetime] = None
    tracking_number: Optional[str] = None
    order_created_at: Optional[datetime] = None

    @field_validator(
        "delivery_date",
        "tracking_number",
        "order_created_at",
        mode="before"
    )
    @classmethod
    def empty_string_to_none(cls, value):
        if value == "":
            return None
        return value

class TimelineEvent(BaseModel):
    event: str
    date: datetime
    source: str

class DerivedFact(BaseModel):
    fact: str
    value: bool
    sources: List[str]

class InvestigationCase(BaseModel):
    dispute: Dispute
    payment: Payment
    merchant_evidence: MerchantEvidence
    timeline: List[TimelineEvent]
    derived_facts: List[DerivedFact]

class Evidence(BaseModel):
    source: str
    fact: str

class InvestigationResult(BaseModel):
    verdict: Literal["MERCHANT_FAVOURED", "CUSTOMER_FAVOURED", "INCONCLUSIVE"]
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str
    evidence: List[Evidence]
    contradictions: List[str]
    recommended_action: str

class DisputeInput(BaseModel):
    dispute: Dispute
    payment: Payment
    merchant_evidence: MerchantEvidence

class InvestigationAnalysis(BaseModel):
    missing_evidence: List[str]
    contradictions: List[str]
    timeline_anomalies: List[str]