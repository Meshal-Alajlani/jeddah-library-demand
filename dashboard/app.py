from pathlib import Path
import sys

import pandas as pd
import streamlit as st
import altair as alt


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
DATA_DIR = ROOT_DIR / "data" / "processed"

sys.path.append(str(SRC_DIR))

from predict import predict_rentals


st.set_page_config(
    page_title="Jeddah Library Forecast",
    page_icon="📚",
    layout="wide"
)


# ─────────────────────────────────────────────────────────────
# Theme state
# ─────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode


dark = st.session_state.dark_mode


# ─────────────────────────────────────────────────────────────
# Theme colors
# ─────────────────────────────────────────────────────────────
if dark:
    BG = "#14100A"
    CARD = "#2A1D12"
    BORDER = "#4A3220"
    TEXT = "#F0E6D6"
    TEXT_SUB = "#C4A882"
    ACCENT = "#C9A97A"
    BTN_BG = "#C9A97A"
    BTN_TEXT = "#14100A"
    DIVIDER = "#3A2818"
    CAPTION = "#9C8064"

    HIGH_BG = "#2D1410"
    HIGH_BORDER = "#C0392B"
    HIGH_TEXT = "#F5C6C0"

    MEDIUM_BG = "#2D2410"
    MEDIUM_BORDER = "#D4A017"
    MEDIUM_TEXT = "#F5E6C0"

    LOW_BG = "#102A18"
    LOW_BORDER = "#2E7D45"
    LOW_TEXT = "#C0F0D0"

    INFO_BG = "#2A1D12"
    INFO_BORDER = "#C9A97A"
    INFO_TEXT = "#F0E6D6"

    CHART_COLOR = "#C9A97A"

else:
    BG = "#F5EFE4"
    CARD = "#EDE3D2"
    BORDER = "#D4BC98"
    TEXT = "#2C1E12"
    TEXT_SUB = "#4A3220"
    ACCENT = "#8B5A2B"
    BTN_BG = "#2C1E12"
    BTN_TEXT = "#F5EFE4"
    DIVIDER = "#D4BC98"
    CAPTION = "#A07850"

    HIGH_BG = "#FBF0E0"
    HIGH_BORDER = "#C0392B"
    HIGH_TEXT = "#4A1C10"

    MEDIUM_BG = "#FBF5E8"
    MEDIUM_BORDER = "#D4A017"
    MEDIUM_TEXT = "#4A3510"

    LOW_BG = "#EAF2EC"
    LOW_BORDER = "#2E7D45"
    LOW_TEXT = "#1A3D22"

    INFO_BG = "#EDE3D2"
    INFO_BORDER = "#8B5A2B"
    INFO_TEXT = "#3D2510"

    CHART_COLOR = "#8B5A2B"


# ─────────────────────────────────────────────────────────────
# Styling
# ─────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700;900&family=Lora:wght@400;500;600&family=Source+Sans+3:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Source Sans 3', sans-serif;
        background-color: {BG};
        color: {TEXT};
    }}

    .stApp {{
        background-color: {BG};
    }}

    #MainMenu, footer, header {{
        visibility: hidden;
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}

    .hero-wrap {{
        border-bottom: 2px solid {ACCENT};
        padding-bottom: 1.4rem;
        margin-bottom: 2rem;
    }}

    .hero-eyebrow {{
        font-family: 'Source Sans 3', sans-serif;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: {ACCENT};
        margin-bottom: 6px;
    }}

    .hero-title {{
        font-family: 'Playfair Display', serif;
        font-size: 52px;
        font-weight: 800;
        color: {TEXT};
        line-height: 1.1;
        margin: 0 0 10px 0;
    }}

    .hero-sub {{
        font-family: 'Source Sans 3', sans-serif;
        font-size: 17px;
        font-weight: 400;
        color: {TEXT_SUB};
        max-width: 680px;
        line-height: 1.6;
    }}

    .section-heading {{
        font-family: 'Playfair Display', serif;
        font-size: 26px;
        font-weight: 700;
        color: {TEXT};
        border-left: 4px solid {ACCENT};
        padding-left: 14px;
        margin: 0 0 1rem 0;
    }}

    .info-card {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 6px;
        padding: 16px 20px;
        font-family: 'Source Sans 3', sans-serif;
        font-size: 15px;
        color: {TEXT_SUB};
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }}

    [data-testid="stMetric"] {{
        background: {CARD} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 6px !important;
        padding: 18px 20px !important;
    }}

    [data-testid="stMetricLabel"] p {{
        font-family: 'Source Sans 3', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        color: {ACCENT} !important;
    }}

    [data-testid="stMetricValue"] {{
        font-family: 'Lora', serif !important;
        font-size: 36px !important;
        font-weight: 600 !important;
        color: {TEXT} !important;
        letter-spacing: 0.01em !important;
    }}

    .result-card {{
        border-radius: 6px;
        padding: 22px 26px;
        font-family: 'Source Sans 3', sans-serif;
        font-size: 16px;
        line-height: 1.7;
        margin-bottom: 12px;
    }}

    .result-card strong {{
        font-size: 17px;
    }}

    .result-high {{
        background: {HIGH_BG};
        border-left: 4px solid {HIGH_BORDER};
        color: {HIGH_TEXT};
    }}

    .result-medium {{
        background: {MEDIUM_BG};
        border-left: 4px solid {MEDIUM_BORDER};
        color: {MEDIUM_TEXT};
    }}

    .result-low {{
        background: {LOW_BG};
        border-left: 4px solid {LOW_BORDER};
        color: {LOW_TEXT};
    }}

    .result-info {{
        background: {INFO_BG};
        border-left: 4px solid {INFO_BORDER};
        color: {INFO_TEXT};
    }}

    .stSelectbox label,
    .stNumberInput label,
    .stSlider label,
    .stDateInput label {{
        font-family: 'Source Sans 3', sans-serif !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        color: {ACCENT} !important;
    }}

    .stSelectbox > div > div > div,
    .stSelectbox [data-baseweb="select"] > div {{
        background-color: {CARD} !important;
        border-color: {BORDER} !important;
        border-radius: 4px !important;
        color: {TEXT} !important;
        cursor: pointer !important;
        font-family: 'Source Sans 3', sans-serif !important;
    }}

    .stSelectbox svg {{
        fill: {ACCENT} !important;
        color: {ACCENT} !important;
    }}

    [data-baseweb="popover"] ul,
    [data-baseweb="menu"] {{
        background-color: {CARD} !important;
        border: 1px solid {BORDER} !important;
    }}

    [data-baseweb="menu"] li {{
        color: {TEXT} !important;
        font-family: 'Source Sans 3', sans-serif !important;
        cursor: pointer !important;
    }}

    [data-baseweb="menu"] li:hover {{
        background-color: {BORDER} !important;
    }}

    .stNumberInput > div > div > input {{
        background-color: {CARD} !important;
        border-color: {BORDER} !important;
        color: {TEXT} !important;
        border-radius: 4px !important;
        font-family: 'Source Sans 3', sans-serif !important;
    }}

    .stNumberInput > div > div > div button {{
        background-color: {BORDER} !important;
        color: {TEXT} !important;
        border-color: {BORDER} !important;
    }}

    .stDateInput > div > div > input {{
        background-color: {CARD} !important;
        border-color: {BORDER} !important;
        color: {TEXT} !important;
        font-family: 'Source Sans 3', sans-serif !important;
    }}

    .stButton > button {{
        background-color: {BTN_BG} !important;
        color: {BTN_TEXT} !important;
        border: none !important;
        border-radius: 6px !important;
        font-family: 'Source Sans 3', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        letter-spacing: 0.14em !important;
        text-transform: uppercase !important;
        padding: 10px 28px !important;
    }}

    .stButton > button:hover {{
        opacity: 0.85 !important;
    }}

    hr {{
        border-color: {DIVIDER} !important;
        margin: 2rem 0 !important;
    }}

    .chart-label {{
        font-family: 'Playfair Display', serif;
        font-size: 18px;
        font-weight: 700;
        color: {TEXT};
        margin-bottom: 6px;
    }}

    .caption-line {{
        font-family: 'Source Sans 3', sans-serif;
        font-size: 12px;
        color: {CAPTION};
        letter-spacing: 0.06em;
        text-align: center;
        padding-top: 1rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    cleaned_data_path = DATA_DIR / "cleaned_library_rentals.csv"
    return pd.read_csv(cleaned_data_path)


def clean_options(series):
    values = series.dropna().astype(str).str.strip()
    values = values[~values.str.lower().isin(["nan", "none", ""])]
    return sorted(values.unique())


def get_demand_level(prediction):
    if prediction >= 60:
        return "High", "high"
    if prediction >= 40:
        return "Medium", "medium"
    return "Low", "low"


def get_suggested_action(prediction):
    if prediction >= 60:
        return "Add extra staff and prepare popular categories before this hour."
    if prediction >= 40:
        return "Keep normal staffing and monitor the branch during this hour."
    return "Keep basic staffing. Use the time for shelving, organizing, or maintenance."


def get_branch_note(prediction, hour):
    if prediction >= 60 and 16 <= hour <= 21:
        return "Busy evening period. The front desk may need faster service."
    if prediction >= 60:
        return "High demand expected. Prepare staff and popular categories early."
    if prediction >= 40:
        return "Balanced demand period. No major changes needed."
    return "Calm period. Good time for internal library tasks."


def build_input_data(
    selected_date, hour, temperature, humidity, wind_speed,
    visibility, solar_radiation, rainfall, season, holiday,
    branch, category, membership, day_of_week,
):
    return {
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
        "Day_of_Week": day_of_week,
    }


data_df = load_data()


# ─────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────
hero_col, toggle_col = st.columns([6, 1])

with hero_col:
    st.markdown(
        """
        <div class="hero-wrap">
            <div class="hero-eyebrow">Jeddah Public Libraries · Demand Forecasting</div>
            <div class="hero-title">📚 Jeddah Library Forecast</div>
            <div class="hero-sub">
                Forecast hourly rental demand and identify peak activity across Jeddah library branches.
                Built to support staffing and branch planning decisions.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with toggle_col:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    theme_label = "☀️ Light" if dark else "🌙 Dark"
    st.button(theme_label, on_click=toggle_theme)


# ─────────────────────────────────────────────────────────────
# Snapshot metrics
# ─────────────────────────────────────────────────────────────
hourly_avg_all = data_df.groupby("Hour")["Rentals_Count"].mean()
peak_hour      = int(hourly_avg_all.idxmax())
peak_value     = round(hourly_avg_all.max(), 1)
branches_count = data_df["Library_Branch"].nunique()
total_records  = f"{len(data_df):,}"

col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    st.metric("Peak Hour", f"{peak_hour}:00")
with col_b:
    st.metric("Avg Rentals at Peak", peak_value)
with col_c:
    st.metric("Branches", branches_count)
with col_d:
    st.metric("Records Used", total_records)

st.divider()


# ─────────────────────────────────────────────────────────────
# Demand estimation
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-heading">Estimate Branch Demand</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="info-card">
        Choose a branch, hour, and daily conditions to estimate expected rentals.
        Model experiments and training history are tracked separately in MLflow.
    </div>
    """,
    unsafe_allow_html=True
)

left, right = st.columns(2, gap="large")

with left:
    selected_date   = st.date_input("Date")
    hour            = st.slider("Hour of Day", 0, 23, 17)
    temperature     = st.number_input("Temperature (°C)", value=34.0)
    humidity        = st.number_input("Humidity (%)", value=55.0)
    wind_speed      = st.number_input("Wind Speed (m/s)", value=4.2)
    visibility      = st.number_input("Visibility (m)", value=1500.0)
    solar_radiation = st.number_input("Solar Radiation (MJ/m²)", value=1.4)
    rainfall        = st.number_input("Rainfall (mm)", value=0.0)

with right:
    season      = st.selectbox("Season",          clean_options(data_df["Season"]))
    holiday     = st.selectbox("Holiday",         clean_options(data_df["Holiday"]))
    branch      = st.selectbox("Library Branch",  clean_options(data_df["Library_Branch"]))
    category    = st.selectbox("Top Category",    clean_options(data_df["Top_Category"]))
    membership  = st.selectbox("Membership Type", clean_options(data_df["Membership_Type"]))
    day_of_week = st.selectbox("Day of Week",     clean_options(data_df["Day_of_Week"]))

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Estimate Demand"):
    input_data = build_input_data(
        selected_date, hour, temperature, humidity, wind_speed,
        visibility, solar_radiation, rainfall, season, holiday,
        branch, category, membership, day_of_week,
    )

    try:
        prediction   = predict_rentals(input_data)
        demand_label, demand_css = get_demand_level(prediction)
        suggested_action = get_suggested_action(prediction)
        branch_note      = get_branch_note(prediction, hour)

        st.divider()
        st.markdown('<div class="section-heading">Demand Summary</div>', unsafe_allow_html=True)

        r1, r2, r3 = st.columns(3)
        with r1:
            st.metric("Expected Rentals", round(prediction, 1))
        with r2:
            st.metric("Demand Level", demand_label)
        with r3:
            st.metric("Hour", f"{hour}:00")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            f'<div class="result-card result-{demand_css}"><strong>Demand outlook:</strong> {branch_note}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="result-card result-info"><strong>Suggested action:</strong> {suggested_action}</div>',
            unsafe_allow_html=True
        )

    except Exception as error:
        st.error(f"Prediction failed: {error}")

st.divider()


# ─────────────────────────────────────────────────────────────
# Demand insights
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-heading">Demand Insights</div>', unsafe_allow_html=True)

insight_1, insight_2 = st.columns(2, gap="large")

with insight_1:
    st.markdown('<p class="chart-label">Average rentals by hour</p>', unsafe_allow_html=True)

    hourly_avg = (
        data_df.groupby("Hour")["Rentals_Count"]
        .mean()
        .round(1)
        .reset_index()
    )

    hourly_avg.columns = ["Hour", "Avg Rentals"]

    hour_chart = (
        alt.Chart(hourly_avg)
        .mark_bar(color=CHART_COLOR)
        .encode(
            x=alt.X("Hour:O", title="Hour"),
            y=alt.Y("Avg Rentals:Q", title="Average Rentals"),
            tooltip=["Hour", "Avg Rentals"]
        )
        .properties(height=330)
    )

    st.altair_chart(hour_chart, use_container_width=True)

with insight_2:
    st.markdown('<p class="chart-label">Average rentals by branch</p>', unsafe_allow_html=True)

    branch_avg = (
        data_df.groupby("Library_Branch")["Rentals_Count"]
        .mean()
        .sort_values(ascending=True)
        .round(1)
        .reset_index()
    )

    branch_avg.columns = ["Library Branch", "Avg Rentals"]

    branch_chart = (
        alt.Chart(branch_avg)
        .mark_bar(color=CHART_COLOR)
        .encode(
            x=alt.X("Avg Rentals:Q", title="Average Rentals"),
            y=alt.Y("Library Branch:N", title="Library Branch", sort="-x"),
            tooltip=["Library Branch", "Avg Rentals"]
        )
        .properties(height=330)
    )

    st.altair_chart(branch_chart, use_container_width=True)

st.divider()


# ─────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────
st.markdown(
    '<div class="caption-line">Meshal Alajlani · Jeddah Library Demand Forecaster · 2026</div>',
    unsafe_allow_html=True
)