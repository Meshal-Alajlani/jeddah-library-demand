from pathlib import Path
import sys

from fastapi import FastAPI
from pydantic import BaseModel


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
sys.path.append(str(SRC_DIR))

from predict import predict_rentals


app = FastAPI(
    title="Jeddah Library Demand API",
    description="API for predicting hourly library rental demand in Jeddah.",
    version="1.0.0"
)


class RentalInput(BaseModel):
    Date: str
    Hour: int
    Temperature_C: float
    Humidity_pct: float
    Wind_Speed_ms: float
    Visibility_m: float
    Solar_Radiation_MJm2: float
    Rainfall_mm: float
    Season: str
    Holiday: str
    Library_Branch: str
    Top_Category: str
    Membership_Type: str
    Day_of_Week: str


@app.get("/")
def home():
    return {
        "message": "Jeddah Library Demand API is running."
    }


@app.post("/predict")
def predict(data: RentalInput):
    input_data = data.model_dump()
    prediction = predict_rentals(input_data)

    return {
        "expected_rentals": round(prediction, 2)
    }