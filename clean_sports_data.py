"""
CSV Data Cleaning Program
Dataset: sports_performance_data(1).csv

What it does:
1. Loads the sports performance CSV file.
2. Removes exact duplicate rows.
3. Cleans text fields and standardizes common missing-value markers.
4. Converts numeric columns to numeric values.
5. Converts Competition_Date to a proper date format.
6. Replaces missing numeric values with the column median.
7. Labels missing categorical/identifier values as "Unknown".
8. Creates a cleaning summary and saves the cleaned CSV.

Run:
    python clean_sports_data.py

Optional:
    python clean_sports_data.py input.csv output.csv
"""

import sys
from pathlib import Path
import pandas as pd


def clean_sports_data(input_file, output_file):
    input_path = Path(input_file)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path.resolve()}\n"
            "Place the CSV in the same folder as this program or provide its full path."
        )

    # Load the dataset
    df = pd.read_csv(input_path)
    original_rows, original_columns = df.shape

    # Standardize blank strings and common missing-value markers
    missing_markers = ["", " ", "NA", "N/A", "na", "n/a", "NULL", "null", "None", "none", "-"]
    df = df.replace(missing_markers, pd.NA)

    # Remove leading/trailing spaces from text columns
    text_columns = df.select_dtypes(include=["object", "string"]).columns
    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()
        df[column] = df[column].replace("", pd.NA)

    # Remove exact duplicate records
    duplicate_count = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    # Convert date column
    if "Competition_Date" in df.columns:
        df["Competition_Date"] = pd.to_datetime(
            df["Competition_Date"], errors="coerce"
        )

    # Convert expected numeric fields (only those present in the file)
    numeric_columns = [
        "Training_Hours_per_Week",
        "Average_Heart_Rate",
        "BMI",
        "Sleep_Hours_per_Night",
        "Daily_Caloric_Intake",
        "Hydration_Level",
        "Previous_Competition_Performance",
        "Resting_Heart_Rate",
        "Body_Fat_Percentage",
        "VO2_Max",
        "Event_Distance",
        "Mental_Focus_Level",
        "Performance_Metric",
    ]

    numeric_columns = [c for c in numeric_columns if c in df.columns]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Treat impossible negative measurements as missing.
    # Values that are merely unusual are retained; they are not automatically deleted.
    non_negative_columns = [
        "Training_Hours_per_Week",
        "Average_Heart_Rate",
        "BMI",
        "Sleep_Hours_per_Night",
        "Daily_Caloric_Intake",
        "Hydration_Level",
        "Previous_Competition_Performance",
        "Resting_Heart_Rate",
        "Body_Fat_Percentage",
        "VO2_Max",
        "Event_Distance",
        "Mental_Focus_Level",
        "Performance_Metric",
    ]
    for column in non_negative_columns:
        if column in df.columns:
            df.loc[df[column] < 0, column] = pd.NA

    # Fill missing numeric values using the median (less sensitive to outliers than mean)
    missing_numeric_before = int(df[numeric_columns].isna().sum().sum())
    for column in numeric_columns:
        if df[column].notna().any():
            df[column] = df[column].fillna(df[column].median())

    # Fill missing text/category fields.
    # IDs and names are not guessed; missing entries are explicitly labelled Unknown.
    category_columns = df.select_dtypes(include=["object", "string"]).columns
    for column in category_columns:
        df[column] = df[column].fillna("Unknown")

    # Save date in a consistent YYYY-MM-DD format
    if "Competition_Date" in df.columns:
        df["Competition_Date"] = df["Competition_Date"].dt.strftime("%Y-%m-%d")
        df["Competition_Date"] = df["Competition_Date"].fillna("Unknown")

    # Save cleaned data
    output_path = Path(output_file)
    df.to_csv(output_path, index=False)

    # Generate a concise cleaning report
    report_path = output_path.with_name(output_path.stem + "_cleaning_report.txt")
    remaining_missing = int(df.isna().sum().sum())

    with report_path.open("w", encoding="utf-8") as report:
        report.write("SPORTS PERFORMANCE DATA - CLEANING REPORT\n")
        report.write("=" * 48 + "\n")
        report.write(f"Input file: {input_path.name}\n")
        report.write(f"Output file: {output_path.name}\n")
        report.write(f"Original rows: {original_rows}\n")
        report.write(f"Rows after removing exact duplicates: {len(df)}\n")
        report.write(f"Exact duplicate rows removed: {duplicate_count}\n")
        report.write(f"Columns: {original_columns}\n")
        report.write(f"Numeric missing/invalid values before filling: {missing_numeric_before}\n")
        report.write(f"Missing values remaining in dataframe: {remaining_missing}\n\n")
        report.write("Missing values by column after cleaning:\n")
        report.write(df.isna().sum().to_string())
        report.write("\n\nNote: Unusual non-negative values are retained for review, not deleted.\n")

    print("Data cleaning completed successfully!")
    print(f"Original shape : ({original_rows}, {original_columns})")
    print(f"Cleaned shape  : {df.shape}")
    print(f"Duplicates removed: {duplicate_count}")
    print(f"Cleaned CSV    : {output_path.resolve()}")
    print(f"Cleaning report: {report_path.resolve()}")


if __name__ == "__main__":
    input_csv = sys.argv[1] if len(sys.argv) > 1 else "sports_performance_data(1).csv"
    output_csv = sys.argv[2] if len(sys.argv) > 2 else "sports_performance_data_cleaned.csv"

    try:
        clean_sports_data(input_csv, output_csv)
    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)
