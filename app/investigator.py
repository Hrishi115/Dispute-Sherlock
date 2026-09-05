from app.models import InvestigationCase, Evidence, InvestigationAnalysis

def analyze_case(case: InvestigationCase) -> InvestigationAnalysis:

    contradictions = []
    missing_evidence = []
    timeline_anomalies = []

    evidence = case.merchant_evidence

    if not evidence.delivery_status:
        missing_evidence.append(
            "Merchant has not provided a delivery status"
        )

    if not evidence.delivery_date:
        missing_evidence.append(
            "Merchant has not provided a delivery date"
        )

    if not evidence.tracking_number:
        missing_evidence.append(
            "No tracking number was provided"
        )

    if not evidence.order_id:
        missing_evidence.append(
            "No order ID was provided"
        )



    delivery_before_dispute = next(
        (
            fact for fact in case.derived_facts
            if fact.fact == "Delivery occurred before dispute was opened"
        ),
        None
    )

    if delivery_before_dispute and not delivery_before_dispute.value:
        timeline_anomalies.append(
            "Delivery occurred after the dispute was opened."
        )

    payment_before_delivery = next(
        (
            fact for fact in case.derived_facts
            if fact.fact == "Payment occurred before delivery"
        ),
        None
    )

    if payment_before_delivery and not payment_before_delivery.value:
        timeline_anomalies.append(
            "Delivery occurred before payment."
        )



    delivery_claimed = (
    evidence.delivery_status
    and "delivered" in evidence.delivery_status.lower()
)

    if (
        delivery_claimed
        and not evidence.delivery_date
    ):
        contradictions.append(
            "Merchant claims the order was delivered, "
            "but no delivery date was provided."
        )

    if (
        case.dispute.reason == "product_not_received"
        and delivery_claimed
    ):
        contradictions.append(
            "Customer claims the product was not received, "
            "while merchant evidence indicates that it was delivered."
        )

    return InvestigationAnalysis(
        missing_evidence=missing_evidence,
        contradictions=contradictions,
        timeline_anomalies=timeline_anomalies
    )