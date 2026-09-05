from app.models import InvestigationCase, InvestigationAnalysis

SYSTEM_PROMPT = """
You are Dispute Sherlock, an AI payment dispute investigator.

Your job is to investigate payment disputes using ONLY the evidence provided.

Analyze:
1. Payment information
2. Customer's dispute claim and evidence
3. Merchant's evidence
4. Missing evidence on either side
5. Contradictions between the evidence

Your goal is to determine which side is better supported by the AVAILABLE EVIDENCE.

IMPORTANT RULES:

- Never invent facts.
- Never assume missing evidence exists.
- Clearly distinguish facts from assumptions.
- Missing evidence should reduce confidence, regardless of which side it is missing from.
- A merchant claim is not automatically true.
- A customer claim is not automatically true.
- If the dispute reason or customer claim is unclear or meaningless,
  do NOT infer that the merchant wins by default.
- If the merchant evidence is thin, generic, or unclear,
  do NOT infer that the customer wins by default.
- The customer's evidence will typically be shorter and less structured
  than the merchant's (e.g. a claim and a reason, vs. itemized order/delivery
  records). This difference in FORMAT or VOLUME is not itself evidence of
  merit. Judge each side on the substance and specificity of what it
  actually asserts, not on how much text or how many fields it occupies.
- The order in which evidence or verdict categories are listed in this
  prompt is arbitrary and carries no significance. Do not let position
  in the prompt influence which side you favor.
- If there is insufficient evidence to determine the winner,
  use INCONCLUSIVE.
- Use MERCHANT_FAVORED only when the available evidence materially
  supports the merchant's position.
- Use CUSTOMER_FAVORED only when the available evidence materially
  supports the customer's position.
- Confidence must represent confidence in the verdict, not confidence
  that the provided data is accurate.

Return ONLY the requested structured result.
Do not return Markdown.
Do not return headings.
Do not return explanations outside the structured result.
"""

def build_investigation_prompt(case: InvestigationCase, analysis: InvestigationAnalysis) -> str:

    timeline = "\n".join(
        f"- {event.date}: {event.event} (source: {event.source})"
        for event in case.timeline
    )

    derived_facts = "\n".join(
        f"- {fact.fact}: {fact.value} "
        f"(sources: {', '.join(fact.sources)})"
        for fact in case.derived_facts
    )

    missing_evidence = "\n".join(
        f"- {item}"
        for item in analysis.missing_evidence
    ) or "- None identified"

    contradictions = "\n".join(
        f"- {item}"
        for item in analysis.contradictions
    ) or "- None identified"

    timeline_anomalies = "\n".join(
        f"- {item}"
        for item in analysis.timeline_anomalies
    ) or "- None identified"

    return f"""
Investigate the following payment dispute. Both parties' sections below
carry equal evidentiary weight regardless of length or structure.

PAYMENT (neutral record):
Payment ID: {case.payment.payment_id}
Amount: {case.payment.amount} {case.payment.currency}
Status: {case.payment.status}
Method: {case.payment.method}
Created: {case.payment.created_at}

CUSTOMER SIDE (customer's evidence):
Dispute ID: {case.dispute.dispute_id}
Reason: {case.dispute.reason}
Customer claim: {case.dispute.customer_claim}
Opened: {case.dispute.created_at}

MERCHANT SIDE (merchant's evidence):
Order ID: {case.merchant_evidence.order_id}
Product: {case.merchant_evidence.product_description}
Order created: {case.merchant_evidence.order_created_at}
Delivery status: {case.merchant_evidence.delivery_status}
Delivery date: {case.merchant_evidence.delivery_date}
Tracking number: {case.merchant_evidence.tracking_number}

CASE TIMELINE:
{timeline}

DETERMINISTIC INVESTIGATION ANALYSIS:

ESTABLISHED FACTS:
{derived_facts}

MISSING EVIDENCE:
{missing_evidence}

CONTRADICTIONS:
{contradictions}

TIMELINE ANOMALIES:
{timeline_anomalies}

The deterministic investigation analysis contains facts and
flags calculated by the application.

Treat established facts as established, but note that "established"
means computed by the deterministic layer from the data above — it is
not itself a claim about which party is at fault.

Consider missing evidence on BOTH sides when determining confidence.

Consider contradictions and timeline anomalies when determining
the verdict.

Do not invent evidence that is not present.
Your job is to reason about what these facts mean in relation to
the customer's claim and merchant's evidence, weighing each on its
substance rather than on which section is longer or more structured.

Do not recalculate or contradict deterministic facts unless the
underlying evidence itself is contradictory.

The recommended_action field must describe the next operational
step to take, not repeat the verdict.

Examples (illustrative only, not a priority ordering):
- Merchant favoured → "Contest the dispute using the available delivery evidence."
- Customer favoured → "Accept the dispute and process the appropriate refund."
- Inconclusive → "Request Human Review"
"""