from pathlib import Path
import sys

import altair as alt
import pandas as pd
import streamlit as st


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
    FIELD_BG = "#21170F"
    BORDER = "#4A3220"
    TEXT = "#F6EBDD"
    TEXT_SUB = "#D5B98E"
    ACCENT = "#C9A97A"
    BTN_BG = "#C9A97A"
    BTN_TEXT = "#14100A"
    DIVIDER = "#3A2818"
    CAPTION = "#B99972"

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
    BG = "#F4EADB"
    CARD = "#E9DDC9"
    FIELD_BG = "#F8F0E4"
    BORDER = "#C9A97A"
    TEXT = "#24180F"
    TEXT_SUB = "#3B2A1E"
    ACCENT = "#8A5527"
    BTN_BG = "#2C1E12"
    BTN_TEXT = "#F8F0E4"
    DIVIDER = "#C9A97A"
    CAPTION = "#7A5638"

    HIGH_BG = "#F7E2D6"
    HIGH_BORDER = "#B53A2E"
    HIGH_TEXT = "#3B160F"

    MEDIUM_BG = "#F4E8C7"
    MEDIUM_BORDER = "#B8870F"
    MEDIUM_TEXT = "#3B2A10"

    LOW_BG = "#E4EFE5"
    LOW_BORDER = "#2E7D45"
    LOW_TEXT = "#173820"

    INFO_BG = "#E9DDC9"
    INFO_BORDER = "#8A5527"
    INFO_TEXT = "#2F2117"

    CHART_COLOR = "#9A632E"


# ─────────────────────────────────────────────────────────────
# Styling
# ─────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <style>
    html, body, [class*="css"] {{
        font-family: "Segoe UI", sans-serif;
        background-color: {BG};
        color: {TEXT};
        font-size: 16px;
        font-weight: 500;
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
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 0.20em;
        text-transform: uppercase;
        color: {ACCENT};
        margin-bottom: 8px;
    }}

    .hero-title {{
        font-family: Georgia, serif;
        font-size: 54px;
        font-weight: 900;
        color: {TEXT};
        line-height: 1.1;
        margin: 0 0 12px 0;
    }}

    .hero-sub {{
        font-size: 19px;
        font-weight: 600;
        color: {TEXT_SUB};
        max-width: 760px;
        line-height: 1.65;
    }}

    .section-heading {{
        font-family: Georgia, serif;
        font-size: 29px;
        font-weight: 900;
        color: {TEXT};
        border-left: 5px solid {ACCENT};
        padding-left: 16px;
        margin: 0 0 1rem 0;
    }}

    .info-card {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 7px;
        padding: 18px 22px;
        font-size: 16px;
        font-weight: 600;
        color: {TEXT_SUB};
        line-height: 1.7;
        margin-bottom: 1.5rem;
    }}

    [data-testid="stMetric"] {{
        background: {CARD} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 7px !important;
        padding: 20px 22px !important;
    }}

    [data-testid="stMetricLabel"] p {{
        font-size: 15px !important;
        font-weight: 800 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: {ACCENT} !important;
    }}

    [data-testid="stMetricValue"] {{
        font-family: "Segoe UI", sans-serif !important;
        font-size: 34px !important;
        font-weight: 650 !important;
        color: {TEXT} !important;
        letter-spacing: 0 !important;
    }}

    .result-card {{
        border-radius: 7px;
        padding: 22px 26px;
        font-size: 18px;
        font-weight: 650;
        line-height: 1.7;
        margin-bottom: 12px;
    }}

    .result-card strong {{
        font-size: 19px;
        font-weight: 900;
    }}

    .result-high {{
        background: {HIGH_BG};
        border-left: 5px solid {HIGH_BORDER};
        color: {HIGH_TEXT};
    }}

    .result-medium {{
        background: {MEDIUM_BG};
        border-left: 5px solid {MEDIUM_BORDER};
        color: {MEDIUM_TEXT};
    }}

    .result-low {{
        background: {LOW_BG};
        border-left: 5px solid {LOW_BORDER};
        color: {LOW_TEXT};
    }}

    .result-info {{
        background: {INFO_BG};
        border-left: 5px solid {INFO_BORDER};
        color: {INFO_TEXT};
    }}

    .stSelectbox label,
    .stNumberInput label,
    .stSlider label,
    .stDateInput label {{
        font-size: 13px !important;
        font-weight: 900 !important;
        letter-spacing: 0.11em !important;
        text-transform: uppercase !important;
        color: {ACCENT} !important;
    }}

    input {{
        background-color: {FIELD_BG} !important;
        color: {TEXT} !important;
        font-weight: 700 !important;
        border: 1px solid {BORDER} !important;
        border-radius: 6px !important;
    }}

    [data-baseweb="input"] {{
        background-color: {FIELD_BG} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 6px !important;
    }}

    [data-baseweb="input"] input {{
        color: {TEXT} !important;
        font-weight: 700 !important;
        background-color: {FIELD_BG} !important;
    }}

    [data-baseweb="select"] > div {{
        background-color: {FIELD_BG} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 6px !important;
        color: {TEXT} !important;
        font-weight: 700 !important;
    }}

    [data-baseweb="select"] span {{
        color: {TEXT} !important;
        font-weight: 700 !important;
    }}

    [data-baseweb="popover"] {{
        background-color: {FIELD_BG} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
    }}

    [role="listbox"] {{
        background-color: {FIELD_BG} !important;
        border: 1px solid {BORDER} !important;
    }}

    [role="option"] {{
        background-color: {FIELD_BG} !important;
        color: {TEXT} !important;
        font-size: 15px !important;
        font-weight: 750 !important;
    }}

    [role="option"]:hover {{
        background-color: {CARD} !important;
        color: {TEXT} !important;
    }}

    [aria-selected="true"] {{
        background-color: {CARD} !important;
        color: {TEXT} !important;
        font-weight: 900 !important;
    }}

    .stButton > button {{
        background-color: {BTN_BG} !important;
        color: {BTN_TEXT} !important;
        border: none !important;
        border-radius: 7px !important;
        font-size: 14px !important;
        font-weight: 900 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        padding: 11px 30px !important;
    }}

    .stButton > button:hover {{
        opacity: 0.88 !important;
    }}

    hr {{
        border-color: {DIVIDER} !important;
        margin: 2.2rem 0 !important;
    }}

    .chart-label {{
        font-family: Georgia, serif;
        font-size: 20px;
        font-weight: 900;
        color: {TEXT};
        margin-bottom: 8px;
    }}

    .caption-line {{
        font-size: 13px;
        font-weight: 700;
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
    selected_date,
    hour,
    temperature,
    humidity,
    wind_speed,
    visibility,
    solar_radiation,
    rainfall,
    season,
    holiday,
    branch,
    category,
    membership,
    day_of_week,
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
        unsafe_allow_html=True,
    )

with toggle_col:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    theme_label = "☀️ Light" if dark else "🌙 Dark"
    st.button(theme_label, on_click=toggle_theme)


# ─────────────────────────────────────────────────────────────
# Snapshot
# ─────────────────────────────────────────────────────────────
hourly_avg_all = data_df.groupby("Hour")["Rentals_Count"].mean()
peak_hour = int(hourly_avg_all.idxmax())
peak_value = round(hourly_avg_all.max(), 1)
branches_count = data_df["Library_Branch"].nunique()
total_records = f"{len(data_df):,}"

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
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns(2, gap="large")

with left:
    selected_date = st.date_input("Date")
    hour = st.slider("Hour of Day", 0, 23, 17)
    temperature = st.number_input("Temperature (°C)", value=34.0)
    humidity = st.number_input("Humidity (%)", value=55.0)
    wind_speed = st.number_input("Wind Speed (m/s)", value=4.2)
    visibility = st.number_input("Visibility (m)", value=1500.0)
    solar_radiation = st.number_input("Solar Radiation (MJ/m²)", value=1.4)
    rainfall = st.number_input("Rainfall (mm)", value=0.0)

with right:
    season = st.selectbox("Season", clean_options(data_df["Season"]))
    holiday = st.selectbox("Holiday", clean_options(data_df["Holiday"]))
    branch = st.selectbox("Library Branch", clean_options(data_df["Library_Branch"]))
    category = st.selectbox("Top Category", clean_options(data_df["Top_Category"]))
    membership = st.selectbox("Membership Type", clean_options(data_df["Membership_Type"]))
    day_of_week = st.selectbox("Day of Week", clean_options(data_df["Day_of_Week"]))

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Estimate Demand"):
    input_data = build_input_data(
        selected_date,
        hour,
        temperature,
        humidity,
        wind_speed,
        visibility,
        solar_radiation,
        rainfall,
        season,
        holiday,
        branch,
        category,
        membership,
        day_of_week,
    )

    try:
        prediction = predict_rentals(input_data)
        demand_label, demand_css = get_demand_level(prediction)
        suggested_action = get_suggested_action(prediction)
        branch_note = get_branch_note(prediction, hour)

        st.divider()
        st.markdown('<div class="section-heading">Demand Summary</div>', unsafe_allow_html=True)

        result_1, result_2, result_3 = st.columns(3)

        with result_1:
            st.metric("Expected Rentals", round(prediction, 1))

        with result_2:
            st.metric("Demand Level", demand_label)

        with result_3:
            st.metric("Hour", f"{hour}:00")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            f'<div class="result-card result-{demand_css}"><strong>Demand outlook:</strong> {branch_note}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="result-card result-info"><strong>Suggested action:</strong> {suggested_action}</div>',
            unsafe_allow_html=True,
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
            tooltip=["Hour", "Avg Rentals"],
        )
        .properties(height=340)
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
            tooltip=["Library Branch", "Avg Rentals"],
        )
        .properties(height=340)
    )

    st.altair_chart(branch_chart, use_container_width=True)


st.divider()


# ─────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────
st.markdown(
    '<div class="caption-line">Meshal Alajlani · Jeddah Library Forecast · 2026</div>',
    unsafe_allow_html=True,
)