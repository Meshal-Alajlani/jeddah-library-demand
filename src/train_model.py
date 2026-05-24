from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor

from data_processing import (
    CATEGORICAL_COLUMNS,
    FEATURE_COLUMNS,
    NUMERIC_COLUMNS,
    clean_data,
    split_features_target,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT_DIR / "data" / "raw" / "jeddah_library_rentals.csv"
MODEL_PATH = ROOT_DIR / "models" / "best_model.pkl"
RESULTS_PATH = ROOT_DIR / "reports" / "model_results.csv"
METADATA_PATH = ROOT_DIR / "models" / "model_metadata.json"


MODEL_CONFIGS = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(max_depth=10, random_state=42),
    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        random_state=42,
        n_jobs=-1,
    ),
    "Neural Network": MLPRegressor(
        hidden_layer_sizes=(32,),
        activation="relu",
        solver="adam",
        max_iter=500,
        random_state=42,
    ),
}


def build_pipeline(model):
    numeric_features = [
        "Hour",
        "Temperature_C",
        "Humidity_pct",
        "Wind_Speed_ms",
        "Visibility_m",
        "Solar_Radiation_MJm2",
        "Rainfall_mm",
        "Month",
        "Day",
        "Is_Peak_Hour",
        "Is_Weekend",
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_COLUMNS),
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )


def evaluate(y_true, y_pred):
    return {
        "R2": round(r2_score(y_true, y_pred), 4),
        "MAE": round(mean_absolute_error(y_true, y_pred), 4),
        "RMSE": round(np.sqrt(mean_squared_error(y_true, y_pred)), 4),
    }


def main():
    df = clean_data(RAW_PATH)
    X, y = split_features_target(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    results = []
    best_model = None
    best_name = None
    best_rmse = float("inf")

    for name, model in MODEL_CONFIGS.items():
        print(f"Training: {name}")
        pipeline = build_pipeline(model)
        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)
        metrics = evaluate(y_test, predictions)
        results.append({"Model": name, **metrics})

        if metrics["RMSE"] < best_rmse:
            best_rmse = metrics["RMSE"]
            best_model = pipeline
            best_name = name

    results_df = pd.DataFrame(results).sort_values("RMSE")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(best_model, MODEL_PATH)
    results_df.to_csv(RESULTS_PATH, index=False)

    metadata = {
        "best_model": best_name,
        "best_rmse": best_rmse,
        "features": FEATURE_COLUMNS,
        "rows_after_cleaning": int(df.shape[0]),
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print("\nModel comparison:")
    print(results_df.to_string(index=False))
    print(f"\nBest model: {best_name}")
    print(f"Saved model to: {MODEL_PATH}")
    print(f"Saved results to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
