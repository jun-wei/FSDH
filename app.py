# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bazi_calculator import calculate_bazi  # import your main logic function

app = FastAPI(title="Bazi API")

class BaziRequest(BaseModel):
    birth_date: str
    birth_time: str
    gender: str = "unknown"

@app.post("/api/bazi")
def get_bazi(data: BaziRequest):
    try:
        result = calculate_bazi(data.birth_date, data.birth_time, data.gender)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
