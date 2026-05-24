from pathlib import Path
import sys

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
REPORTS_DIR = ROOT_DIR / "reports"
DATA_DIR = ROOT_DIR / "data" / "processed"

sys.path.append(str(SRC_DIR))

from predict import predict_rentals


st.set_page_config(
    page_title="Jeddah Library Demand Advisor",
    page_icon="📚",
    layout="wide"
)


def clean_options(series):
    values = series.dropna().astype(str).str.strip()
    values = values[~values.str.lower().isin(["nan", "none", ""])]
    return sorted(values.unique())


def get_recommendation(prediction):
    if prediction >= 60:
        return "High expected demand. Add more staff during this hour."
    elif prediction >= 40:
        return "Medium expected demand. Normal staffing should be enough."
    else:
        return "Low expected demand. Keep basic staffing only."


results_path = REPORTS_DIR / "model_results.csv"
cleaned_data_path = DATA_DIR / "cleaned_library_rentals.csv"

results_df = pd.read_csv(results_path)
data_df = pd.read_csv(cleaned_data_path)

best_model = results_df.sort_values(by="R2", ascending=False).iloc[0]

st.title("Jeddah Library Demand Advisor")
st.write(
    "A machine learning system that predicts hourly library rental demand "
    "and helps library managers make better staffing decisions."
)

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Best Model", best_model["Model"])

with col2:
    st.metric("R2 Score", round(best_model["R2"], 4))

with col3:
    st.metric("MAE", round(best_model["MAE"], 4))

with col4:
    st.metric("RMSE", round(best_model["RMSE"], 4))

st.subheader("Model Performance")

left_chart, right_table = st.columns([1.2, 1])

with left_chart:
    st.write("R2 score comparison")
    st.bar_chart(results_df.set_index("Model")["R2"])

with right_table:
    st.write("Evaluation results")
    st.dataframe(results_df, use_container_width=True)

st.divider()

st.subheader("Demand Insights")

hourly_avg = data_df.groupby("Hour")["Rentals_Count"].mean()
st.write("Average rentals by hour")
st.line_chart(hourly_avg, use_container_width=True)

branch_avg = (
    data_df.groupby("Library_Branch")["Rentals_Count"]
    .mean()
    .sort_values(ascending=False)
)

st.write("Average rentals by branch")
st.bar_chart(branch_avg, use_container_width=True)

st.divider()

st.subheader("What-if Demand Prediction")
st.write("Change the values below to estimate the expected number of rentals.")

left, right = st.columns(2)

with left:
    selected_date = st.date_input("Date")
    hour = st.slider("Hour", 0, 23, 17)
    temperature = st.number_input("Temperature C", value=34.0)
    humidity = st.number_input("Humidity Percent", value=55.0)
    wind_speed = st.number_input("Wind Speed", value=4.2)
    visibility = st.number_input("Visibility", value=1500.0)
    solar_radiation = st.number_input("Solar Radiation", value=1.4)
    rainfall = st.number_input("Rainfall", value=0.0)

with right:
    season = st.selectbox("Season", clean_options(data_df["Season"]))
    holiday = st.selectbox("Holiday", clean_options(data_df["Holiday"]))
    branch = st.selectbox("Library Branch", clean_options(data_df["Library_Branch"]))
    category = st.selectbox("Top Category", clean_options(data_df["Top_Category"]))
    membership = st.selectbox("Membership Type", clean_options(data_df["Membership_Type"]))
    day_of_week = st.selectbox("Day of Week", clean_options(data_df["Day_of_Week"]))

if st.button("Predict Demand"):
    input_data = {
        "Date": selected_date.strftime("%d/%m/%Y"),
        "Hour": hour,
        "Temperature_C": temperature,
        "Humidity_pct": humidity,
        "Wind_Speed_ms": wind_speed,
        "Visibility_m": visibility,
        "Solar_Radiation_MJm2": solar_radiation,
        "Rainfall_mm": rainfall,
        "Season": season,
        "Holiday": holiday,
        "Library_Branch": branch,
        "Top_Category": category,
        "Membership_Type": membership,
        "Day_of_Week": day_of_week
    }

    prediction = predict_rentals(input_data)
    recommendation = get_recommendation(prediction)

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        st.success(f"Expected rentals: {round(prediction, 2)}")

    with result_col2:
        st.info(recommendation)

st.divider()

st.caption(
    "Built with Python, Scikit-learn, FastAPI, Streamlit, and GitHub."
)