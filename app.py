# app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bazi_calculator import calculate_bazi

app = FastAPI(title="BaZi API")

class BaziRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    surname: str
    csv_path: str
    best_elements: list = None

@app.get("/")
def root():
    return {"message": "BaZi API is running"}

@app.post("/calculate")
def calculate_bazi_endpoint(request: BaziRequest):
    try:
        result = calculate_bazi(
            request.year, request.month, request.day, request.hour,
            request.surname, request.csv_path, request.best_elements
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
