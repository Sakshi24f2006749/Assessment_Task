import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def create_features(df):
    """
    Create analytical and ML-oriented features.
    """

    # ---------------------------------
    # Recency Calculation
    # ---------------------------------

    latest_date = df["Session_Date"].max()

    df["Recency"] = (
        latest_date - df["Session_Date"]
    ).dt.days

    # ---------------------------------
    # Conversion Flag
    # ---------------------------------

    df["Conversion_Flag"] = np.where(
        df["Purchase_Value"] > 0,
        1,
        0
    )

    # ---------------------------------
    # Engagement Score
    # ---------------------------------

    df["Engagement_Score"] = (
        (df["Page_Views"] * 0.4)
        +
        ((df["Dwell_Time_Secs"] / 60) * 0.6)
    ).round(2)

    # ---------------------------------
    # High Value Customer
    # ---------------------------------

    df["High_Value_Customer"] = np.where(
        df["Purchase_Value"] >= 4000,
        1,
        0
    )

    # ---------------------------------
    # Purchase Prediction
    # ---------------------------------

    df["Purchase_Prediction"] = np.where(
        (
            (df["Page_Views"] >= 5)
            &
            (df["Dwell_Time_Secs"] >= 180)
        ),
        1,
        0
    )

    return df


if __name__ == "__main__":

    from extract import extract_data
    from transform import clean_data

    df = extract_data(
        BASE_DIR / "data" / "messy_user_activity.xlsx"
)

    cleaned_df, metrics = clean_data(df)

    featured_df = create_features(cleaned_df)

    print("\nFEATURE ENGINEERING COMPLETE")
    print("=" * 50)

    print(
        featured_df[
            [
                "User_ID",
                "Recency",
                "Engagement_Score",
                "Conversion_Flag",
                "High_Value_Customer",
                "Purchase_Prediction"
            ]
        ].head()
    )