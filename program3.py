import os
import pandas as pd


def inspect_dataset(df: pd.DataFrame) -> None:
    """Prints structural dimensions, data types, missing values,

    and statistical summaries of the loaded dataset.
    """
    print("\n" + "=" * 50)
    print("DATASET STRUCTURAL INSPECTION")
    print("=" * 50)

    # 1. Structural Dimensions
    rows, cols = df.shape
    print(f"Shape: {rows} rows, {cols} columns")

    # 2. Schema and Missing Values
    print("\n--- Column Metadata & Null Counts ---")
    meta_df = pd.DataFrame(
        {
            "Data Type": df.dtypes,
            "Null Count": df.isnull().sum(),
            "Null Ratio (%)": (df.isnull().sum() / rows * 100).round(2),
        }
    )
    print(meta_df)

    # 3. Numeric Summary
    print("\n--- Numerical Summary Statistics ---")
    numeric_summary = df.describe()
    if not numeric_summary.empty:
        print(numeric_summary.round(2))
    else:
        print("No numerical columns detected.")
    print("=" * 50 + "\n")


def filter_and_clean_data(
    df: pd.DataFrame,
    query_condition: str | None = None,
    drop_nulls: bool = True,
) -> pd.DataFrame:
    """Cleans missing records and applies dynamic logical filter queries.

    Example query_condition: "age > 25 and salary >= 50000"
    """
    processed_df = df.copy()

    # Drop missing rows if flagged
    if drop_nulls:
        initial_count = len(processed_df)
        processed_df = processed_df.dropna()
        dropped = initial_count - len(processed_df)
        print(f"[Clean] Dropped {dropped} rows containing null values.")

    # Apply expression filter if specified
    if query_condition:
        try:
            processed_df = processed_df.query(query_condition)
            print(f"[Filter] Applied condition: '{query_condition}'")
        except Exception as e:
            print(f"[Warning] Failed to apply query '{query_condition}': {e}")

    print(f"[Status] Processed rows remaining: {len(processed_df)}")
    return processed_df


def export_dataset(
    df: pd.DataFrame, output_path: str, file_format: str = "csv"
) -> None:
    """Exports processed data to specified formats (csv, json, or parquet)."""
    fmt = file_format.lower()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    if fmt == "csv":
        df.to_csv(output_path, index=False)
    elif fmt == "tsv":
        df.to_csv(output_path, sep="\t", index=False)
    elif fmt == "json":
        df.to_json(output_path, orient="records", indent=2)
    elif fmt == "parquet":
        df.to_parquet(output_path, index=False)
    else:
        raise ValueError(f"Unsupported format: '{file_format}'")

    print(f"[Export] Saved clean dataset to: {output_path} ({fmt.upper()})")


def run_pipeline(
    filepath: str,
    output_path: str,
    query_filter: str | None = None,
    export_fmt: str = "csv",
) -> None:
    """Orchestrates ingestion, inspection, transformation, and export."""
    # Read dynamic separator (auto-detects comma, tab, semicolon)
    print(f"[Ingestion] Loading: {filepath}")
    df = pd.read_csv(filepath, sep=None, engine="python")

    # Step 1: Structural Inspection
    inspect_dataset(df)

    # Step 2: Clean & Filter
    filtered_df = filter_and_clean_data(
        df, query_condition=query_filter, drop_nulls=True
    )

    # Step 3: Export Sub-Data
    export_dataset(filtered_df, output_path=output_path, file_format=export_fmt)

# Example Usage & Verification
if __name__ == "__main__":
    # Create sample CSV for testing
    sample_file = "raw_sample_data.csv"
    exported_file = "clean_export_data.json"

    raw_test_data = """id,department,score,salary,active
101,Engineering,88.5,75000,True
102,Marketing,,52000,True
103,Engineering,92.0,88000,True
104,HR,64.0,45000,False
105,Engineering,79.0,61000,True
106,Finance,95.5,91000,True
"""
    with open(sample_file, "w") as f:
        f.write(raw_test_data)

    # Run complete pipeline:
    # Keeps Engineering or Finance departments with score > 80, drops nulls, exports as JSON
    run_pipeline(
        filepath=sample_file,
        output_path=exported_file,
        query_filter="score > 80.0 and active == True",
        export_fmt="json",
    )

    # Cleanup test files
    if os.path.exists(sample_file):
        os.remove(sample_file)
    if os.path.exists(exported_file):
        os.remove(exported_file)