"""
Data inspection module for MarketMosaic.

This module provides functions to inspect and analyze marketing datasets,
specifically Google's Meridian Marketing Mix Modeling dataset.

Functions:
    load_data: Load CSV data into a pandas DataFrame
    get_basic_info: Display basic dataset information
    get_data_types: Show column data types and categorization
    check_missing_values: Calculate missing value statistics
    check_duplicates: Count duplicate rows
    main: Execute all inspection functions
"""

import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, Optional


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV data from the specified file path.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        pandas DataFrame containing the loaded data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        pd.errors.EmptyDataError: If the file is empty
        pd.errors.ParserError: If there's an error parsing the CSV
    """
    try:
        # Convert to Path object for better path handling
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Load the CSV file
        print(f"📂 Loading data from: {path}")
        df = pd.read_csv(path)
        
        # Check if DataFrame is empty
        if df.empty:
            print("⚠️ Warning: Loaded an empty DataFrame")
        
        print(f"✅ Successfully loaded {len(df)} rows and {len(df.columns)} columns")
        return df
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        raise
    except pd.errors.EmptyDataError:
        print("❌ Error: The CSV file is empty")
        raise
    except pd.errors.ParserError as e:
        print(f"❌ Error parsing CSV: {e}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise


def get_basic_info(df: pd.DataFrame) -> Dict[str, any]:
    """
    Get basic information about the dataset.
    
    Args:
        df: pandas DataFrame to analyze
        
    Returns:
        Dictionary containing basic dataset information
    """
    print("\n" + "="*60)
    print("📊 BASIC DATASET INFORMATION")
    print("="*60)
    
    info = {
        'shape': df.shape,
        'columns': list(df.columns),
        'sample': df.head()
    }
    
    print(f"Dataset dimensions: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\nColumn names ({len(df.columns)} total):")
    
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    print(f"\nFirst 5 rows:")
    print(df.head())
    
    return info


def get_data_types(df: pd.DataFrame) -> Dict[str, list]:
    """
    Analyze and categorize column data types.
    
    Args:
        df: pandas DataFrame to analyze
        
    Returns:
        Dictionary with categorized column lists
    """
    print("\n" + "="*60)
    print("🔧 DATA TYPE ANALYSIS")
    print("="*60)
    
    # Get all data types
    print("Column data types:")
    print(df.dtypes)
    
    # Categorize columns
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Check if time column exists (might be string)
    time_cols = [
        col
        for col in df.columns
        if any(token in col.lower() for token in ('time', 'date'))
    ]
    
    categories = {
        'numerical': numerical_cols,
        'categorical': categorical_cols,
        'datetime': datetime_cols,
        'time_related': time_cols
    }
    
    print(f"\n📈 Numerical columns ({len(numerical_cols)}):")
    for col in numerical_cols[:10]:  # Show first 10
        print(f"  - {col}")
    if len(numerical_cols) > 10:
        print(f"  ... and {len(numerical_cols) - 10} more")
    
    print(f"\n🏷️  Categorical columns ({len(categorical_cols)}):")
    for col in categorical_cols:
        print(f"  - {col}")
    
    print(f"\n📅 Time-related columns ({len(time_cols)}):")
    for col in time_cols:
        print(f"  - {col}")
    
    return categories


def check_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Check for missing values in the dataset.
    
    Args:
        df: pandas DataFrame to analyze
        
    Returns:
        DataFrame with missing value statistics
    """
    print("\n" + "="*60)
    print("❓ MISSING VALUE ANALYSIS")
    print("="*60)
    
    # Calculate missing values
    missing_counts = df.isnull().sum()
    missing_percent = (missing_counts / len(df) * 100).round(2)
    
    # Create summary DataFrame
    missing_df = pd.DataFrame({
        'Missing Count': missing_counts,
        'Missing %': missing_percent
    })
    
    # Filter to only show columns with missing values
    columns_with_missing = missing_df[missing_df['Missing Count'] > 0]
    
    if len(columns_with_missing) == 0:
        print("✅ No missing values found in the dataset!")
        return missing_df
    
    print(f"⚠️ Found {len(columns_with_missing)} columns with missing values:")
    print(columns_with_missing)
    
    total_missing = missing_counts.sum()
    total_cells = df.shape[0] * df.shape[1]
    overall_missing_percent = (total_missing / total_cells * 100).round(2)
    
    print(f"\n📊 Overall missing data: {total_missing:,} cells ({overall_missing_percent}%)")
    
    return missing_df


def check_duplicates(df: pd.DataFrame) -> Dict[str, int]:
    """
    Check for duplicate rows in the dataset.
    
    Args:
        df: pandas DataFrame to analyze
        
    Returns:
        Dictionary with duplicate statistics
    """
    print("\n" + "="*60)
    print("🔍 DUPLICATE ROW ANALYSIS")
    print("="*60)
    
    # Check for exact duplicates
    duplicate_count = df.duplicated().sum()
    duplicate_percent = (duplicate_count / len(df) * 100).round(2)
    
    print(f"Exact duplicate rows: {duplicate_count} ({duplicate_percent}%)")
    
    if duplicate_count > 0:
        print("\nFirst 5 duplicate rows:")
        duplicates = df[df.duplicated(keep=False)]  # keep=False shows all duplicates
        print(duplicates.head())
    
    # Check for duplicates based on key columns (excluding index)
    key_columns = [col for col in df.columns if col != 'Unnamed: 0']
    if len(key_columns) > 0:
        key_duplicates = df.duplicated(subset=key_columns).sum()
        key_duplicate_percent = (key_duplicates / len(df) * 100).round(2)
        print(f"\nDuplicates based on key columns: {key_duplicates} ({key_duplicate_percent}%)")
    
    results = {
        'exact_duplicates': duplicate_count,
        'exact_duplicate_percent': duplicate_percent,
        'total_rows': len(df)
    }
    
    return results


def main():
    """
    Main function to execute all data inspection steps.
    """
    print("="*60)
    print("MARKETMOSAIC - DATA INSPECTION MODULE")
    print("="*60)
    
    try:
        # Load the data
        data_path = "data/raw/geo_all_channels.csv"
        df = load_data(data_path)
        
        # Perform all inspections
        basic_info = get_basic_info(df)
        data_types = get_data_types(df)
        missing_values = check_missing_values(df)
        duplicates = check_duplicates(df)
        
        print("\n" + "="*60)
        print("✅ DATA INSPECTION COMPLETE")
        print("="*60)
        
        # Summary
        print("\n📋 INSPECTION SUMMARY:")
        print(f"  • Dataset: {basic_info['shape'][0]:,} rows × {basic_info['shape'][1]} columns")
        print(f"  • Numerical columns: {len(data_types['numerical'])}")
        print(f"  • Categorical columns: {len(data_types['categorical'])}")
        print(f"  • Missing values: {missing_values['Missing Count'].sum():,} cells")
        print(f"  • Duplicate rows: {duplicates['exact_duplicates']}")
        
        # Return the DataFrame for further use
        return df
        
    except Exception as e:
        print(f"\n❌ Inspection failed: {e}")
        return None


if __name__ == "__main__":
    # This runs when the script is executed directly
    main()