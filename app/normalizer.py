from app.models import (
    Dispute,
    Payment,
    MerchantEvidence,
    InvestigationCase,
    TimelineEvent,
    DerivedFact
)


def normalize_case(
        dispute: Dispute,
        payment: Payment,
        merchant_evidence: MerchantEvidence
) -> InvestigationCase:

    timeline = []

    timeline.append(TimelineEvent(
        event="payment captured",
        date=payment.created_at,
        source="payment"
    ))

    if merchant_evidence.order_created_at:
        timeline.append(TimelineEvent(
            event="order_created_at",
            date=merchant_evidence.order_created_at,
            source="merchant"
        ))

    if merchant_evidence.delivery_date:
        timeline.append(TimelineEvent(
            event=merchant_evidence.delivery_status or "delivery_event",
            date=merchant_evidence.delivery_date,
            source="merchant"
        ))

    timeline.append(TimelineEvent(
        event="dispute_opened",
        date=dispute.created_at,
        source="dispute"
    ))

    timeline.sort(key=lambda event: event.date)

    derived_facts = []

    derived_facts.append(DerivedFact(
        fact="Payment was successfully captured",
        value=payment.status.lower() == "captured",
        sources=["payment.status"]
    ))

    derived_facts.append(DerivedFact(
        fact="Order is marked as delivered",
        value=merchant_evidence.delivery_status == "delivered",
        sources=["merchant_evidence.delivery_status"]
    ))

    if merchant_evidence.delivery_date:

        derived_facts.append(DerivedFact(
            fact="Payment occurred before delivery",
            value=merchant_evidence.delivery_date >= payment.created_at,
            sources=[
                "merchant_evidence.delivery_date",
                "payment.created_at"
            ]
        ))

        derived_facts.append(DerivedFact(
            fact="Delivery occurred before dispute was opened",
            value=merchant_evidence.delivery_date <= dispute.created_at,
            sources=[
                "merchant_evidence.delivery_date",
                "dispute.created_at"
            ]
        ))

    return InvestigationCase(
        dispute=dispute,
        payment=payment,
        merchant_evidence=merchant_evidence,
        timeline=timeline,
        derived_facts=derived_facts
    )