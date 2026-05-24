# Jeddah Library Demand Forecasting System

This project predicts hourly library rental demand for public library branches in Jeddah.

## Goal

Help library management plan staffing and inventory by predicting the expected number of book rentals per hour.

## Current Version

This is the first working version of the project.

It includes:

- Data cleaning
- Feature engineering
- Model training
- Model comparison
- Best model saving
- Simple prediction script

## Models Used

- Linear Regression
- Decision Tree
- Random Forest
- Neural Network

## Project Structure

```text
data/raw/
data/processed/
models/
reports/
src/
```

## How to Run

Create the cleaned dataset:

```bash
python src/clean_data.py
```

Train the models:

```bash
python src/train_model.py
```

Run a sample prediction:

```bash
python src/predict.py
```

## Next Steps

- Add an API using FastAPI
- Add a dashboard using Streamlit
- Add experiment tracking using MLflow
- Add Docker
- Add Airflow to run the full pipeline
