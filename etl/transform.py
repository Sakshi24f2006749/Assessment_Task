import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def clean_data(df):
    """
    Cleans the raw dataset and returns:
    1. Cleaned DataFrame
    2. ETL Metrics Dictionary
    """

    metrics = {}

    # ----------------------------
    # Initial Metrics
    # ----------------------------
    metrics["rows_before_cleaning"] = len(df)

    # ----------------------------
    # Missing Values Count
    # ----------------------------
    metrics["missing_values_handled"] = int(df.isnull().sum().sum())

    # ----------------------------
    # Remove Exact Duplicates
    # ----------------------------
    duplicates = df.duplicated().sum()

    df = df.drop_duplicates()

    metrics["duplicates_removed"] = int(duplicates)

    # ----------------------------
    # Fix Invalid Dwell Time
    # ----------------------------
    df.loc[df["Dwell_Time_Secs"] < 0, "Dwell_Time_Secs"] = np.nan

    # ----------------------------
    # Standardize Device Categories
    # ----------------------------
    device_mapping = {
        "desktop": "Desktop",
        "DESKTOP": "Desktop",
        "Desktop": "Desktop",
        "mobile": "Mobile",
        "MOBILE": "Mobile",
        "Mobile": "Mobile",
        "tab": "Tablet",
        "TAB": "Tablet",
        "Tab": "Tablet"
    }

    df["Device_Category"] = df["Device_Category"].replace(device_mapping)

    # ----------------------------
    # Handle Missing Values
    # ----------------------------

    # Page Views
    df["Page_Views"] = df["Page_Views"].fillna(
        df["Page_Views"].median()
    )

    # Dwell Time
    df["Dwell_Time_Secs"] = df["Dwell_Time_Secs"].fillna(
        df["Dwell_Time_Secs"].median()
    )

    # Purchase Value
    df["Purchase_Value"] = df["Purchase_Value"].fillna(0)

    # Location
    df["Location_Code"] = df["Location_Code"].fillna("Unknown")

    # Session Date
    df["Session_Date"] = pd.to_datetime(
        df["Session_Date"],
        errors="coerce"
    )

    df["Session_Date"] = df["Session_Date"].fillna(
        df["Session_Date"].mode()[0]
    )

    # ----------------------------
    # Final Metrics
    # ----------------------------
    metrics["rows_after_cleaning"] = len(df)

    return df, metrics


if __name__ == "__main__":

    from extract import extract_data

    df = extract_data(
        BASE_DIR / "data" / "messy_user_activity.xlsx"
)

    cleaned_df, metrics = clean_data(df)

    print("\nCLEANING METRICS")
    print("=" * 50)

    for key, value in metrics.items():
        print(f"{key}: {value}")

    print("\nCleaned Data Preview")
    print(cleaned_df.head())