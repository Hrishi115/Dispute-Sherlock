from pydantic import BaseModel
from typing import List, Optional, Literal

class Payment(BaseModel):
    payment_id: str
    amount: float
    currency: str
    status: str
    method: str

class Dispute(BaseModel):
    dispute_id: str
    reason: str
    customer_claim: str

class MerchantEvidence(BaseModel):
    order_id: Optional[str] = None
    product_description: Optional[str] = None
    delivery_status: Optional[str] = None
    delivery_date: Optional[str] = None
    tracking_number: Optional[str] = None

class InvestigationCase(BaseModel):
    dispute: Dispute
    payment: Payment
    merchant_evidence: MerchantEvidence

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
