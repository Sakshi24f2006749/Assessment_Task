import pandas as pd


def extract_data(file_path):
    """
    Reads the raw Excel dataset and returns a DataFrame.
    """

    try:
        df = pd.read_excel(file_path)

        print("=" * 50)
        print("DATA EXTRACTION SUCCESSFUL")
        print("=" * 50)
        print(f"Rows Loaded: {len(df)}")
        print(f"Columns Found: {list(df.columns)}")

        return df

    except Exception as e:
        print(f"Error reading file: {e}")
        return None


if __name__ == "__main__":
    data = extract_data(r"C:\Users\saksh\Videos\Assessment_Task\data\messy_user_activity.xlsx")

    if data is not None:
        print("\nFirst 5 Rows:")
        print(data.head())