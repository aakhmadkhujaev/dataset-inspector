import os
import pandas as pd

def load_dataset():
    while True:
        file_path = input("Enter the path to the dataset (CSV file): ")

        try:
            df = pd.read_csv(file_path)

            return df, file_path

        except Exception as e:
            print(f"Error loading dataset: {e}. Please try again.")

def show_shape(df, file_path):

    file_name = os.path.basename(file_path)

    numeric_df = df.select_dtypes(include="number")
    categorical_df = df.select_dtypes(include=["object", "string"])

    print("\n========================================")
    print("          DATASET OVERVIEW")
    print("========================================")

    print(f"Dataset             : {file_name}")
    print(f"Rows                : {df.shape[0]}")
    print(f"Columns             : {df.shape[1]}")
    print(f"Numeric Columns     : {numeric_df.shape[1]}")
    print(f"Categorical Columns : {categorical_df.shape[1]}")

def show_info(df):

    print("\n========================================")
    print("       DATASET INFO REPORT")
    print("========================================")

    for column, dtype in df.dtypes.items():
        print(f"{column:<15} : {dtype}")


def get_preview_rows():
    while True:
        try:
            n = int(input("Enter the number of rows to preview: "))
            if n > 0:
                return n
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def show_head(df, n):
    total_rows = df.shape[0]
    if n > total_rows:
        print(f"Requested number of rows exceeds total rows in the dataset. Showing all {total_rows} rows.")
        n = total_rows
    preview = df.head(n)
    print(preview)
    return preview


def show_missing_values(df):

    print("========================================")
    print(  "=== DATASET MISSING VALUES REPORT ===" )
    print("========================================") 

    # 1. Count missing values
    missing_count = df.isnull().sum()

    # 2. Keep only problematic columns
    missing_count = missing_count[missing_count > 0]

    # 3. Handle datasets with no missing values
    if len(missing_count) == 0:
        print("No missing values found.")
        return None

    # 4. Calculate percentages
    missing_percentage = (missing_count / len(df)) * 100

    # 5. Build report
    report = pd.DataFrame({
        "Missing Count": missing_count,
        "Missing %": missing_percentage
    })

    # 6. Sort by highest missing percentage
    report = report.sort_values(
        by="Missing %",
        ascending=False
    )

    # 7. Show report
    print(report)

    # 8. Return report
    return report

def show_duplicates(df):
    print("========================================")
    print("\n=== DATASET DUPLICATE ROWS REPORT ===")
    print("========================================")
    duplicate_rows = df[df.duplicated()]

    if duplicate_rows.empty:
        print("No duplicate rows found.")
        return None

    duplicate_count = len(duplicate_rows)

    print(f"Duplicate rows found: {duplicate_count}")

    print("\nPreview of duplicate rows:")
    print(duplicate_rows.head())

    return duplicate_rows

def show_unique_values(df):
    print("========================================")
    print("\n=== DATASET UNIQUE VALUES REPORT   ===")
    print("========================================")

    categorical_df = df.select_dtypes(include=["object", "string"])
    unique_counts = categorical_df.nunique()
    for column, count in unique_counts.items():
        print(f"{column:<10} : {count} unique values")
    return unique_counts

def show_statistics(df):
    print("========================================")
    print("\n===   DATASET STATISTICS REPORT    ===")  
    print("========================================")
    numeric_df = df.select_dtypes(include="number")
    stats = numeric_df.describe().round(1)
    print(stats)
    return stats

def show_outliers(df):

    print("========================================")
    print("\n===    DATASET OUTLIER REPORT      ===")
    print("========================================")

    numeric_df = df.select_dtypes(include="number")

    outlier_report = {}

    for column in numeric_df:

        # Calculate Q1
        q1 = numeric_df[column].quantile(0.25)

        # Calculate Q3
        q3 = numeric_df[column].quantile(0.75)

        # Calculate IQR
        iqr = q3 - q1

        # Calculate bounds
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Count outliers
        outlier_count = numeric_df[(numeric_df[column] < lower_bound) | (numeric_df[column] > upper_bound)].shape[0]

        # Store if count > 0
        if outlier_count > 0:
            outlier_report[column] = outlier_count
           

    if len(outlier_report) == 0:
        print("No outliers found.")
        return None

    for column, count in outlier_report.items():
        print(f"{column:<12} : {count} outliers")

    return outlier_report
def ask_continue():

    while True:

        choice = input(
            "\nInspect another dataset? (y/n): "
        ).strip().lower()

        if choice in ["y", "yes"]:
            return True

        if choice in ["n", "no"]:
            return False

        print("Please enter y or n.")


def inspect_dataset(df, file_path):
    
    show_shape(df, file_path)
    show_info(df)
    n = get_preview_rows()
    show_head(df, n)

    show_missing_values(df)
    show_duplicates(df)

    show_unique_values(df)
    show_statistics(df)

    show_outliers(df)

    print("\n========================================")
    print("       INSPECTION COMPLETE                ")
    print("==========================================")
    print("✓ Shape analyzed")
    print("✓ Missing values checked")
    print("✓ Duplicate rows checked")
    print("✓ Unique values analyzed")
    print("✓ Statistics generated")
    print("✓ Outliers detected")

def main():

    while True:

        df, file_path = load_dataset()

        inspect_dataset(df, file_path)

        if not ask_continue():
            break
    
if __name__ == "__main__":
    main()