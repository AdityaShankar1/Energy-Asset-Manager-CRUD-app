import pandas as pd
import os
import sys
from typing import Optional

# --- Configuration ---
# 1. Input Path (Confirmed .csv)
RAW_FILE_PATH = "/Users/adityashankar/Downloads/india-crude-oil-indicators.csv"

# 2. Output Path
BASE_DIR = os.path.dirname(RAW_FILE_PATH)
FILE_NAME_BASE = os.path.splitext(os.path.basename(RAW_FILE_PATH))[0]
CLEANED_FILE_NAME = FILE_NAME_BASE + "_cleaned.csv"
CLEANED_FILE_PATH = os.path.join(BASE_DIR, CLEANED_FILE_NAME)

# --- Robust Cleaning Function ---

def clean_kapsarc_data(input_filepath: str, output_filepath: Optional[str] = None) -> pd.DataFrame:
    """
    Loads, cleans, and optionally saves the crude oil indicator data.
    """
    print(f"Loading data from: {input_filepath}")
    
    try:
        # **THE FIX: Using semicolon (;) as the separator**
        df = pd.read_csv(input_filepath, sep=';') 
    except FileNotFoundError:
        print(f"\nFATAL ERROR: The file was not found at: {input_filepath}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"\nFATAL ERROR: Could not read file contents. Check file integrity.", file=sys.stderr)
        raise

    # 1. Normalize Column Names (Removes leading/trailing spaces from headers)
    df.columns = df.columns.str.strip() 

    # Define the key columns we must have
    TIME_COL = 'Time Period'
    VALUE_COL = 'OBS_VALUE'
    
    # Check for critical column presence
    if TIME_COL not in df.columns:
        print(f"\nFATAL ERROR: Column '{TIME_COL}' not found. Actual columns found: {df.columns.tolist()}", file=sys.stderr)
        raise KeyError(f"Missing critical column: {TIME_COL}")

    # 2. Convert 'Time Period' to datetime
    df[TIME_COL] = pd.to_datetime(df[TIME_COL], errors='coerce')

    # 3. Clean and convert 'OBS_VALUE'
    if VALUE_COL in df.columns:
        df[VALUE_COL] = pd.to_numeric(
            df[VALUE_COL],
            errors='coerce'
        ).fillna(0.0).astype(float)
    else:
        print(f"Warning: Column '{VALUE_COL}' not found.", file=sys.stderr)
    
    # 4. Trim whitespace from all remaining string columns
    for col in df.select_dtypes(include=['object']).columns:
        if not df[col].isnull().all():
            df[col] = df[col].astype(str).str.strip()

    # Save the cleaned data (saving it back as a standard comma-separated CSV)
    if output_filepath:
        print(f"Saving cleaned data to: {output_filepath}")
        df.to_csv(output_filepath, index=False)
    
    print("Data cleaning complete.")
    return df


# --- Execute the Script ---

if __name__ == "__main__":
    try:
        # Load, clean, and save the data in one step
        cleaned_df = clean_kapsarc_data(
            input_filepath=RAW_FILE_PATH,
            output_filepath=CLEANED_FILE_PATH
        )
        
        print("\n--- Sample of Cleaned Data ---")
        print(cleaned_df.head())
        
    except (FileNotFoundError, KeyError):
        # Errors are printed inside the function, exit gracefully
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected runtime error occurred: {e}", file=sys.stderr)
        sys.exit(1)
