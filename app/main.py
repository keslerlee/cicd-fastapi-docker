from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI(title="System Metric Validator Service", version="1.0.0")

START_TIME = time.time()

class PayloadData(BaseModel):
    batch_id: str
    record_count: int
    status: str

@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "service": "metric-validator"
    }

@app.post("/validate")
def validate_payload(data: PayloadData):
    if data.record_count < 0:
        raise HTTPException(status_code=400, detail="record_count cannot be negative")

    is_valid = data.status.lower() in ["active", "pending", "complete"]
    return {
        "batch_id": data.batch_id,
        "processed_records": data.record_count,
        "is_valid_status": is_valid
    }