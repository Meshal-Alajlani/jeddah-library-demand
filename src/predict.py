from pathlib import Path
import joblib
import pandas as pd

from data_processing import add_features, FEATURE_COLUMNS


ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT_DIR / "models" / "best_model.pkl"


def predict_rentals(input_data: dict) -> float:
    model = joblib.load(MODEL_PATH)

    row = pd.DataFrame([input_data])
    row["Date"] = pd.to_datetime(row["Date"], dayfirst=True)
    row = add_features(row)
    row = row[FEATURE_COLUMNS]

    prediction = model.predict(row)[0]
    return round(float(prediction), 2)


if __name__ == "__main__":
    sample = {
        "Date": "24/05/2026",
        "Hour": 17,
        "Temperature_C": 34,
        "Humidity_pct": 55,
        "Wind_Speed_ms": 4.2,
        "Visibility_m": 1500,
        "Solar_Radiation_MJm2": 1.4,
        "Rainfall_mm": 0,
        "Season": "Summer",
        "Holiday": "No",
        "Library_Branch": "University Branch",
        "Top_Category": "Technology",
        "Membership_Type": "Student",
        "Day_of_Week": "Sunday",
    }

    result = predict_rentals(sample)
    print(f"Expected rentals: {result}")
