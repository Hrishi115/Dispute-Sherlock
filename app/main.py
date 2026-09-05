from fastapi import FastAPI
from models import InvestigationCase

app = FastAPI()

@app.get("/")
async def health_check():
    return {"status":"ok"}

@app.post("/investigate")
async def investigate(case: InvestigationCase):
    return {
        "message": "Investigation Case recieved",
        "case": case
    }