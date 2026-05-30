# Jeddah Library Forecast

A machine learning project that forecasts hourly book rental demand for public library branches in Jeddah.

The project includes a trained prediction model, a FastAPI prediction service, a Streamlit dashboard, Docker support, Airflow automation, MLflow experiment tracking, and a live Hugging Face demo.

## Live Demo

https://huggingface.co/spaces/ITMeshal/jeddah-library-forecast

## Project Goal

The goal is to help library managers estimate demand by hour and make better staffing and branch planning decisions.

The system predicts expected rentals using:

- Date and hour
- Weather data
- Library branch
- Book category
- Membership type
- Holiday status
- Day of week

## Features

- Data cleaning and feature engineering
- Model training and comparison
- Best model saving
- FastAPI prediction API
- Streamlit dashboard
- MLflow experiment tracking
- Airflow pipeline automation
- Docker Compose setup
- Hugging Face dashboard demo

## Models

The project compares four models:

| Model | R2 | MAE | RMSE |
|---|---:|---:|---:|
| Neural Network | 0.9411 | 3.5722 | 5.1040 |
| Random Forest | 0.9203 | 4.2967 | 5.9376 |
| Linear Regression | 0.8629 | 6.0693 | 7.7858 |
| Decision Tree | 0.8613 | 5.9150 | 7.8324 |

Best model:

**Neural Network**

## Project Structure

```text
jeddah-library-demand/
├── api/
├── dashboard/
├── airflow/
├── data/
├── models/
├── reports/
├── src/
├── Dockerfile
├── Dockerfile.airflow
├── docker-compose.yml
├── docker-compose.airflow.yml
├── requirements.txt
├── streamlit_app.py
└── README.md
```

## Run with Docker

Make sure Docker Desktop is running.

```bash
docker compose up --build
```

Open:

```text
Dashboard: http://127.0.0.1:8501
API:       http://127.0.0.1:8000
MLflow:    http://127.0.0.1:5000
```

Stop containers:

```bash
docker compose down
```

## Run Manually

Install dependencies:

```bash
pip install -r requirements.txt
```

Clean data:

```bash
python src/clean_data.py
```

Train models:

```bash
python src/train_model.py
```

Run sample prediction:

```bash
python src/predict.py
```

Run API:

```bash
python -m uvicorn api.main:app --reload
```

Run dashboard:

```bash
python -m streamlit run dashboard/app.py
```

Run MLflow:

```bash
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root mlartifacts --host 127.0.0.1 --port 5000
```

## API Example

Endpoint:

```text
POST /predict
```

Example response:

```json
{
  "expected_rentals": 92.84
}
```

## Airflow Pipeline

Start Airflow:

```bash
docker compose -f docker-compose.airflow.yml up --build
```

Open:

```text
http://127.0.0.1:8080
```

Login:

```text
username: admin
password: admin
```

Pipeline tasks:

```text
preprocess_library_data → train_and_evaluate_models → validate_prediction_output
```

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- FastAPI
- Streamlit
- Altair
- Docker
- Apache Airflow
- MLflow
- Hugging Face Spaces

## Future Improvements

- Add an architecture diagram
- Add dashboard screenshots to the README
