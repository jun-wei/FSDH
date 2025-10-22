# app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bazi_calculator import calculate_bazi

app = FastAPI(title="BaZi Five Elements API")

class BaziRequest(BaseModel):
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour: int
    birth_minute: int

@app.get("/")
def root():
    return {"message": "BaZi Five Elements API is running"}

@app.post("/bazi")
def bazi_endpoint(req: BaziRequest):
    try:
        result = calculate_bazi(
            req.birth_year, req.birth_month, req.birth_day, req.birth_hour, req.birth_minute
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
