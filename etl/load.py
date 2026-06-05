import sqlite3
import pandas as pd


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "database" / "analytics.db"


def create_database():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    PRAGMA foreign_keys = ON;
    """)

    # -----------------------------
    # USERS TABLE
    # -----------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        location_code TEXT
    )
    """)

    # -----------------------------
    # ANALYTICS TABLE
    # -----------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analytics (
        analytics_id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id TEXT,

        session_date DATE,

        page_views REAL,

        dwell_time_secs REAL,

        device_category TEXT,

        purchase_value REAL,

        recency INTEGER,

        conversion_flag INTEGER,

        engagement_score REAL,

        high_value_customer INTEGER,

        purchase_prediction INTEGER,

        FOREIGN KEY(user_id)
        REFERENCES users(user_id)
    )
    """)

    # -----------------------------
    # ETL METRICS TABLE
    # -----------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS etl_metrics (

        metric_name TEXT PRIMARY KEY,

        metric_value TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Database & Tables Created Successfully")


def load_users(df):

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users"
)

    conn.commit()
    users_df = df[
        ["User_ID", "Location_Code"]
    ].drop_duplicates()

    users_df.columns = [
        "user_id",
        "location_code"
    ]

    users_df.to_sql(
        "users",
        conn,
        if_exists="append",
        index=False
)

    conn.close()

    print("Users Loaded")


def load_analytics(df):

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM analytics"
)

    conn.commit()
    analytics_df = pd.DataFrame()

    analytics_df["user_id"] = df["User_ID"]
    analytics_df["session_date"] = df["Session_Date"]
    analytics_df["page_views"] = df["Page_Views"]
    analytics_df["dwell_time_secs"] = df["Dwell_Time_Secs"]
    analytics_df["device_category"] = df["Device_Category"]
    analytics_df["purchase_value"] = df["Purchase_Value"]

    analytics_df["recency"] = df["Recency"]
    analytics_df["conversion_flag"] = df["Conversion_Flag"]
    analytics_df["engagement_score"] = df["Engagement_Score"]
    analytics_df["high_value_customer"] = df["High_Value_Customer"]
    analytics_df["purchase_prediction"] = df["Purchase_Prediction"]

    analytics_df.to_sql(
        "analytics",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()

    print("Analytics Loaded")


def load_etl_metrics(metrics):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM etl_metrics")

    for key, value in metrics.items():

        cursor.execute(
            """
            INSERT INTO etl_metrics
            VALUES (?, ?)
            """,
            (key, str(value))
        )

    conn.commit()
    conn.close()

    print("ETL Metrics Loaded")


if __name__ == "__main__":

    from extract import extract_data
    from transform import clean_data
    from feature_engineering import create_features

    df = extract_data(
        BASE_DIR / "data" / "messy_user_activity.xlsx"
)

    cleaned_df, metrics = clean_data(df)

    featured_df = create_features(cleaned_df)

    create_database()

    load_users(featured_df)

    load_analytics(featured_df)

    load_etl_metrics(metrics)

    print("\nDATABASE LOAD COMPLETE")