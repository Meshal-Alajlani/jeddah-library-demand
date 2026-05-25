# Jeddah Library Demand Advisor

This project is an end-to-end machine learning system that predicts hourly library rental demand for public library branches in Jeddah.

The goal is to help library managers make better staffing and inventory decisions using data instead of guessing.

---

## Project Overview

The system predicts the expected number of book rentals per hour based on:

- Date
- Hour
- Weather data
- Library branch
- Book category
- Membership type
- Holiday status
- Day of week

The project also provides a simple staffing recommendation based on the predicted demand.

Example:

```text
Expected rentals: 63.24
High expected demand. Add more staff during this hour.
```

---

## Current Features

- Data cleaning
- Feature engineering
- Model training
- Model comparison
- Best model saving
- Sample prediction script
- Prediction API
- Interactive dashboard
- Docker support
- Airflow training pipeline
- Daily automated pipeline schedule
- Demand insights
- Staffing recommendation

---

## Models Used

The project trains and compares four machine learning models:

- Linear Regression
- Decision Tree
- Random Forest
- Neural Network

The best model is selected based on the evaluation results.

---

## Model Results

| Model | R2 | MAE | RMSE |
|---|---:|---:|---:|
| Neural Network | 0.9411 | 3.5722 | 5.1040 |
| Random Forest | 0.9203 | 4.2967 | 5.9376 |
| Linear Regression | 0.8629 | 6.0693 | 7.7858 |
| Decision Tree | 0.8613 | 5.9150 | 7.8324 |

Best model:

**Neural Network**

---

## Project Structure

```text
jeddah-library-demand/
│
├── airflow/
│   └── dags/
│       └── library_pipeline.py
│
├── api/
│   └── main.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   │   └── jeddah_library_rentals.csv
│   └── processed/
│       └── cleaned_library_rentals.csv
│
├── models/
│   ├── best_model.pkl
│   └── model_metadata.json
│
├── reports/
│   └── model_results.csv
│
├── src/
│   ├── clean_data.py
│   ├── data_processing.py
│   ├── predict.py
│   └── train_model.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── Dockerfile.airflow
├── docker-compose.yml
├── docker-compose.airflow.yml
├── README.md
└── requirements.txt
```

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/Meshal-Alajlani/jeddah-library-demand.git
```

Go inside the project folder:

```bash
cd jeddah-library-demand
```

---

### 2. Install Requirements

Install all required Python libraries:

```bash
pip install -r requirements.txt
```

---

### 3. Clean the Data

Run the data cleaning script:

```bash
python src/clean_data.py
```

This will create the cleaned dataset here:

```text
data/processed/cleaned_library_rentals.csv
```

---

### 4. Train the Models

Run the training script:

```bash
python src/train_model.py
```

This will:

- Train the machine learning models
- Compare their performance
- Select the best model
- Save the best model

The best model will be saved here:

```text
models/best_model.pkl
```

The model results will be saved here:

```text
reports/model_results.csv
```

---

### 5. Run a Sample Prediction

Run:

```bash
python src/predict.py
```

Example output:

```text
Expected rentals: 92.84
```

---

## Run the API

The API allows users to send input data and get a rental demand prediction.

Start the API server:

```bash
python -m uvicorn api.main:app --reload
```

Open this link in the browser:

```text
http://127.0.0.1:8000
```

You should see:

```json
{
  "message": "Jeddah Library Demand API is running."
}
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## API Prediction Example

Go to:

```text
http://127.0.0.1:8000/docs
```

Open:

```text
POST /predict
```

Click:

```text
Try it out
```

Use this example input:

```json
{
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
  "Day_of_Week": "Sunday"
}
```

Example response:

```json
{
  "expected_rentals": 92.84
}
```

---

## Run the Dashboard

The dashboard provides a visual interface for model results, demand insights, and what-if prediction.

Start the dashboard:

```bash
python -m streamlit run dashboard/app.py
```

The browser will open the dashboard automatically.

The dashboard includes:

- Best model result
- Model comparison
- Average rentals by hour
- Average rentals by branch
- What-if demand prediction form
- Staffing recommendation

Example output:

```text
Expected rentals: 63.24
High expected demand. Add more staff during this hour.
```

---

## Run with Docker

This project can also be started using Docker.

Make sure Docker Desktop is running.

Build and start the containers:

```bash
docker compose up --build
```

After the containers start, open:

```text
http://127.0.0.1:8000
```

For the API.

Open:

```text
http://127.0.0.1:8501
```

For the dashboard.

To stop the containers, press:

```text
Ctrl + C
```

Or run:

```bash
docker compose down
```

---

## Run the Airflow Pipeline

This project includes an Airflow pipeline that automates the machine learning workflow.

The pipeline runs these tasks:

```text
preprocess_library_data
↓
train_and_evaluate_models
↓
validate_prediction_output
```

The DAG is scheduled to run daily.

Make sure Docker Desktop is running.

Start Airflow:

```bash
docker compose -f docker-compose.airflow.yml up --build
```

Open Airflow in the browser:

```text
http://127.0.0.1:8080
```

Login:

```text
username: admin
password: admin
```

Find the DAG:

```text
library_demand_training_pipeline
```

You can run it manually by clicking the play button.

To stop Airflow, press:

```text
Ctrl + C
```

Then run:

```bash
docker compose -f docker-compose.airflow.yml down
```

---

## Main Commands Summary

Install libraries:

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

Run API and dashboard with Docker:

```bash
docker compose up --build
```

Stop Docker containers:

```bash
docker compose down
```

Run Airflow:

```bash
docker compose -f docker-compose.airflow.yml up --build
```

Stop Airflow:

```bash
docker compose -f docker-compose.airflow.yml down
```

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- FastAPI
- Streamlit
- Docker
- Docker Compose
- Apache Airflow
- Joblib
- Git
- GitHub

---

## Why This Project Matters

Many small organizations make daily staffing and inventory decisions based on guessing.

This project shows how machine learning can support better operational decisions by predicting demand and giving simple recommendations.

Instead of only building a model, this project turns the model into a usable system with:

- A training pipeline
- A saved best model
- An API
- An interactive dashboard
- Dockerized services
- An Airflow automation pipeline
- A decision recommendation

---

## Next Steps

- Add MLflow experiment tracking
- Improve dashboard design
- Add deployment option
- Create an architecture diagram