from fastapi import FastAPI
from openrouter import OpenRouter
import os
from dotenv import load_dotenv
load_dotenv()

from app.models import InvestigationCase, InvestigationResult, DisputeInput
from app.normalizer import normalize_case
from app.investigator import analyze_case
from app.prompts import build_investigation_prompt, SYSTEM_PROMPT

app = FastAPI()

client = OpenRouter(
    api_key = os.environ["OPENROUTER_API_KEY"]
)

@app.get("/")
async def health_check():
    return {"status":"ok"}

@app.post("/investigate")
async def investigate(data: DisputeInput):

    print("1. Request Recieved")
    case = normalize_case(
        data.dispute,
        data.payment,
        data.merchant_evidence
    )

    print("2. Normalization complete")

    analysis = analyze_case(case)

    print("3. Analysis complete")

    prompt = build_investigation_prompt(case, analysis)

    print("4. Prompt built")

    response = client.chat.send(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "investigation_result",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "verdict": {
                        "type": "string",
                        "enum": [
                            "MERCHANT_FAVOURED",
                            "CUSTOMER_FAVOURED",
                            "INCONCLUSIVE"
                        ]
                    },
                    "confidence": {
                        "type": "number"
                    },
                    "summary": {
                        "type": "string"
                    },
                    "evidence": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "source": {
                                    "type": "string"
                                },
                                "fact": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "source",
                                "fact"
                            ],
                            "additionalProperties": False
                        }
                    },
                    "contradictions": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "recommended_action": {
                        "type": "string"
                    }
                },
                "required": [
                    "verdict",
                    "confidence",
                    "summary",
                    "evidence",
                    "contradictions",
                    "recommended_action"
                ],
                "additionalProperties": False
                }
            }
        }
    )

    print("5. LLM response received")

    result = InvestigationResult.model_validate_json(response.choices[0].message.content)

    print("6. Result validated")
    
    return result

    # return case.model_dump_json()