from app.models import InvestigationCase, InvestigationResult

def investigator(case: InvestigationCase) -> InvestigationResult:
    evidence = []
    contradictions = []

    if case.payment.status == "captured":
        evidence.append({
            "source": "payment",
            "fact": "Payment was successfully captured"
        })

    if case.merchant_evidence.delivery_status == "delivered":
        evidence.append({
            "source": "merchant",
            "fact": "Merchant evidence says that the order was delivered"
        })

    if (case.dispute.reason == "product not recieved" and case.merchant_evidence.delivery_status == "delivered"):
        return InvestigationResult(
            verdict = "MERCHANT_FAVOURED",
            confidence = 0.90,
            summary= "Available evidence proves that the disputed order was delivered",
            evidence=evidence,
            contradictions=contradictions,
            recommended_action="contest the dispute with delivery evidence"
        )

    return InvestigationResult(
        verdict = "INCONCLUSIVE",
        confidence= 0.40,
        summary = "There is not sufficient evidence to determine the outcome confidently",
        evidence=evidence,
        contradictions= contradictions,
        recommended_action="Request more evidence from the merchant"
    )

