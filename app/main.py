from fastapi import FastAPI
from app.models import InvestigationCase, InvestigationResult
# from app.investigator import investigator
from app.prompts import build_investigation_prompt, SYSTEM_PROMPT
from openrouter import OpenRouter
import json
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

client = OpenRouter(
    api_key = os.environ["OPENROUTER_API_KEY"]
)

@app.get("/")
async def health_check():
    return {"status":"ok"}

@app.post("/investigate")
async def investigate(case: InvestigationCase):

    prompt = build_investigation_prompt(case)

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
                            "MERCHANT_FAVORED",
                            "CUSTOMER_FAVORED",
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

    result = InvestigationResult.model_validate_json(response.choices[0].message.content)
    
    return result

    # return response.choices[0].message.content