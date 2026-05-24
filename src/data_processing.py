from pathlib import Path
import numpy as np
import pandas as pd


NUMERIC_COLUMNS = [
    "Temperature_C",
    "Humidity_pct",
    "Wind_Speed_ms",
    "Visibility_m",
    "Solar_Radiation_MJm2",
    "Rainfall_mm",
]

CATEGORICAL_COLUMNS = [
    "Season",
    "Holiday",
    "Library_Branch",
    "Top_Category",
    "Membership_Type",
    "Day_of_Week",
    "Temperature_Bin",
]

FEATURE_COLUMNS = [
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
    "Season",
    "Holiday",
    "Library_Branch",
    "Top_Category",
    "Membership_Type",
    "Day_of_Week",
    "Temperature_Bin",
]

TARGET_COLUMN = "Rentals_Count"


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["Is_Peak_Hour"] = df["Hour"].apply(
        lambda h: 1 if (9 <= h <= 11) or (16 <= h <= 19) else 0
    )
    df["Temperature_Bin"] = df["Temperature_C"].apply(
        lambda t: "Cool" if t < 25 else ("Warm" if t <= 35 else "Hot")
    )
    df["Is_Weekend"] = df["Date"].dt.weekday.isin([4, 5]).astype(int)

    return df


def clean_data(input_path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(input_path)

    # Fix date column.
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["Date"]).copy()

    # Fix numeric columns.
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.loc[df["Temperature_C"] < 0, "Temperature_C"] = np.nan
    df.loc[df["Rentals_Count"] < 0, "Rentals_Count"] = np.nan

    for col in NUMERIC_COLUMNS + [TARGET_COLUMN]:
        df[col] = df[col].fillna(df[col].median())

    # Standardize text columns.
    for col in ["Library_Branch", "Top_Category", "Season", "Membership_Type"]:
        df[col] = df[col].astype(str).str.strip().str.title()

    yes_no_map = {
        "Y": "Yes", "Yes": "Yes", "yes": "Yes", "YES": "Yes",
        "N": "No", "No": "No", "no": "No", "NO": "No",
    }
    df["Holiday"] = df["Holiday"].map(yes_no_map).fillna("No")
    df["Functioning_Day"] = df["Functioning_Day"].map(yes_no_map).fillna("Yes")

    df["Season"] = df["Season"].replace("", np.nan).fillna("Unknown")
    df["Membership_Type"] = df["Membership_Type"].replace("", np.nan).fillna("Regular")

    if "Snowfall_cm" in df.columns:
        df = df.drop(columns=["Snowfall_cm"])

    df = df.drop_duplicates().copy()
    df = df[df["Functioning_Day"] == "Yes"].copy()
    df = df.reset_index(drop=True)

    df = add_features(df)
    return df


def split_features_target(df: pd.DataFrame):
    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()
    return X, y
