# 🕵️ Dispute Sherlock

### AI-Powered Payment Dispute Investigator

Dispute Sherlock investigates payment disputes by combining payment data, customer claims, and merchant evidence into a structured, evidence-backed decision.

## The Problem

Chargeback investigation often requires manually correlating:

* Payment and transaction records
* Customer dispute claims
* Merchant order and delivery evidence
* Event timelines
* Missing or contradictory information

This makes investigations slow and difficult to standardize.

## The Solution

Dispute Sherlock automates the investigation workflow.

```text
Payment + Dispute + Merchant Evidence
                ↓
          Case Normalization
                ↓
       Deterministic Analysis
                ↓
          AI Investigation
                ↓
       Structured Decision
```

The system first builds a normalized investigation case and performs deterministic checks for:

* Missing evidence
* Contradictions
* Timeline anomalies
* Derived facts from the available data

The resulting investigation context is then provided to the AI investigator.

## Output

Each investigation produces:

* **Verdict**

  * `MERCHANT_FAVOURED`
  * `CUSTOMER_FAVOURED`
  * `INCONCLUSIVE`
* **Confidence score**
* **Investigation summary**
* **Supporting evidence**
* **Detected contradictions**
* **Recommended action**

The output is validated against a strict structured schema before being returned.

## Architecture

```text
                ┌──────────────────────┐
                │    Dispute Input     │
                │ Payment + Customer + │
                │ Merchant Evidence    │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │    Case Normalizer   │
                │ Timeline + Derived   │
                │ Facts                │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │ Deterministic        │
                │ Investigation Layer  │
                │                      │
                │ • Missing Evidence   │
                │ • Contradictions     │
                │ • Timeline Anomalies │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │    AI Investigator   │
                │   OpenRouter / LLM   │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │   Structured Result  │
                │ Verdict + Evidence + │
                │ Confidence + Action  │
                └──────────────────────┘
```

## Tech Stack

* **Python**
* **FastAPI**
* **Pydantic**
* **OpenRouter**
* **GPT-OSS 20B**
* **python-dotenv**

## How It Works

### 1. Case Normalization

Raw payment, dispute, and merchant data is converted into a structured investigation case.

The system also constructs a chronological timeline and derives facts such as whether payment occurred before delivery or whether delivery occurred before the dispute was opened.

### 2. Deterministic Investigation

Before involving the LLM, the application checks the case for:

* Missing merchant evidence
* Contradictions
* Timeline anomalies
* Relevant derived facts

This provides the AI with a structured view of the case rather than raw, unprocessed input.

### 3. AI Investigation

The AI investigator evaluates the customer's claim and merchant evidence using the structured investigation context.

It is explicitly instructed to:

* Use only the provided evidence
* Never invent facts
* Consider missing evidence
* Consider contradictions
* Consider timeline anomalies
* Use `INCONCLUSIVE` when the available evidence is insufficient

### 4. Structured Output

The final response is constrained to a strict JSON schema containing the verdict, confidence, reasoning, evidence, contradictions, and recommended action.

## API

### `POST /investigate`

Accepts:

* Dispute information
* Payment information
* Merchant evidence

Returns a structured investigation result.

### Health Check

```text
GET /
```

Returns:

```json
{
  "status": "ok"
}
```

## Running Locally

### Requirements

* Python 3.x
* OpenRouter API key

### Setup

```bash
git clone https://github.com/Hrishi115/Dispute-Sherlock.git
cd Dispute-Sherlock

python -m venv .venv
```

Activate the environment:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Start the API:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## Evaluation

The system was evaluated against **24 test cases**.

**3 cases were excluded because the inputs were invalid**, leaving **21 valid cases**.

### Result

**12 / 21 correct — 57.1% accuracy**

The evaluation showed stronger performance on cases with clear supporting evidence and weaker performance on ambiguous, contradictory, and temporally anomalous cases.

The evaluation dataset is included in [`eval.xlsx`](eval.xlsx).

## Project Structure

```text
Dispute-Sherlock/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── normalizer.py
│   ├── investigator.py
│   └── prompts.py
│
├── reports/
├── eval.xlsx
├── LICENSE
└── README.md
```

## Core Design Principle

> **The AI reasons over evidence; the application prepares and validates the investigation context.**

Dispute Sherlock separates deterministic evidence analysis from AI reasoning, allowing the system to combine predictable data processing with flexible evidence-based investigation.

## Built for Razorpay Buildathon

**Track:** AI Risk Manager

**Project:** Dispute Sherlock
