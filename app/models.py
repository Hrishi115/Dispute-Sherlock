from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import date

class Payment(BaseModel):
    payment_id: str
    amount: float
    currency: str
    status: str
    method: str
    created_at: str

class Dispute(BaseModel):
    dispute_id: str
    reason: str
    customer_claim: str
    created_at: str

class MerchantEvidence(BaseModel):
    order_id: Optional[str] = None
    product_description: Optional[str] = None
    delivery_status: Optional[str] = None
    delivery_date: Optional[str] = None
    tracking_number: Optional[str] = None
    order_created_at: str

class TimelineEvent(BaseModel):
    event: str
    date: date
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
    confidence: float
    summary: str
    evidence: List[Evidence]
    contradictions: List[str]
    recommended_action: str

class DisputeInput(BaseModel):
    dispute: Dispute
    payment: Payment
    merchant_evidence: MerchantEvidence