from extract import extract_data
from transform import clean_data
from feature_engineering import create_features
from load import (
    create_database,
    load_users,
    load_analytics,
    load_etl_metrics
)

from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "messy_user_activity.xlsx"


def run_pipeline():

    print("\n" + "=" * 60)
    print("STARTING ETL PIPELINE")
    print("=" * 60)

    # --------------------------------
    # Extract
    # --------------------------------

    df = extract_data(DATA_PATH)

    if df is None:
        print("Pipeline Failed During Extraction")
        return

    # --------------------------------
    # Transform
    # --------------------------------

    cleaned_df, metrics = clean_data(df)

    metrics["etl_run_timestamp"] = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)

    # --------------------------------
    # Feature Engineering
    # --------------------------------

    featured_df = create_features(cleaned_df)

    # --------------------------------
    # Database Load
    # --------------------------------

    create_database()

    load_users(featured_df)

    load_analytics(featured_df)

    load_etl_metrics(metrics)

    print("\n" + "=" * 60)
    print("ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print("\nPipeline Metrics")

    for key, value in metrics.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    run_pipeline()