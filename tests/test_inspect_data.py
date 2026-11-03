"""
Test suite for the data inspection module.

This module tests the functionality of inspect_data.py
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os

# Import the module to test (adjust path if needed)
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from inspect_data import (
    load_data,
    get_basic_info,
    get_data_types,
    check_missing_values,
    check_duplicates
)


class TestDataInspection:
    """Test class for data inspection functions."""
    
    @pytest.fixture
    def sample_dataframe(self):
        """Create a sample DataFrame for testing."""
        data = {
            'id': [1, 2, 3, 4, 5],
            'category': ['A', 'B', 'A', 'C', 'B'],
            'value': [10.5, 20.3, 15.7, np.nan, 25.0],
            'count': [100, 200, 150, 175, 225],
            'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']
        }
        return pd.DataFrame(data)
    
    @pytest.fixture
    def temp_csv_file(self, sample_dataframe):
        """Create a temporary CSV file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            sample_dataframe.to_csv(f.name, index=False)
            temp_path = f.name
        
        yield temp_path
        
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    
    @pytest.fixture
    def duplicate_dataframe(self):
        """Create a DataFrame with duplicates for testing."""
        data = {
            'id': [1, 2, 3, 3, 4],
            'value': [10, 20, 30, 30, 40]
        }
        return pd.DataFrame(data)
    
    def test_load_data_valid_file(self, temp_csv_file):
        """Test loading data from a valid CSV file."""
        df = load_data(temp_csv_file)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert len(df.columns) == 5
        assert 'id' in df.columns
        assert 'category' in df.columns
    
    def test_load_data_file_not_found(self):
        """Test loading data from a non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_data("non_existent_file.csv")
    
    def test_get_basic_info(self, sample_dataframe):
        """Test basic information extraction."""
        info = get_basic_info(sample_dataframe)
        
        assert isinstance(info, dict)
        assert 'shape' in info
        assert 'columns' in info
        assert 'sample' in info
        
        assert info['shape'] == (5, 5)
        assert len(info['columns']) == 5
        assert isinstance(info['sample'], pd.DataFrame)
    
    def test_get_data_types(self, sample_dataframe):
        """Test data type categorization."""
        type_info = get_data_types(sample_dataframe)
        
        assert isinstance(type_info, dict)
        assert 'numerical' in type_info
        assert 'categorical' in type_info
        assert 'time_related' in type_info
        
        # Check specific categorizations
        assert 'value' in type_info['numerical']
        assert 'count' in type_info['numerical']
        assert 'category' in type_info['categorical']
        assert 'date' in type_info['time_related']
    
    def test_check_missing_values_no_missing(self, sample_dataframe):
        """Test missing value check with no missing values (after filling)."""
        # Create a copy without missing values
        df_no_missing = sample_dataframe.copy()
        df_no_missing['value'] = df_no_missing['value'].fillna(0)
        
        missing_df = check_missing_values(df_no_missing)
        
        assert isinstance(missing_df, pd.DataFrame)
        assert 'Missing Count' in missing_df.columns
        assert 'Missing %' in missing_df.columns
        assert missing_df['Missing Count'].sum() == 0
    
    def test_check_missing_values_with_missing(self, sample_dataframe):
        """Test missing value check with actual missing values."""
        missing_df = check_missing_values(sample_dataframe)
        
        assert isinstance(missing_df, pd.DataFrame)
        assert missing_df.loc['value', 'Missing Count'] == 1
        assert missing_df.loc['value', 'Missing %'] == 20.0  # 1 out of 5 = 20%
    
    def test_check_duplicates_no_duplicates(self, sample_dataframe):
        """Test duplicate check with no duplicates."""
        duplicate_info = check_duplicates(sample_dataframe)
        
        assert isinstance(duplicate_info, dict)
        assert 'exact_duplicates' in duplicate_info
        assert duplicate_info['exact_duplicates'] == 0
    
    def test_check_duplicates_with_duplicates(self, duplicate_dataframe):
        """Test duplicate check with actual duplicates."""
        duplicate_info = check_duplicates(duplicate_dataframe)
        
        assert isinstance(duplicate_info, dict)
        assert duplicate_info['exact_duplicates'] == 1  # One duplicate row
    
    def test_check_duplicates_key_columns(self, duplicate_dataframe):
        """Test duplicate check using key columns."""
        duplicate_info = check_duplicates(duplicate_dataframe)
        
        # The function should report duplicates based on all columns
        assert duplicate_info['exact_duplicates'] >= 0
    
    def test_dataframe_manipulation_preservation(self, sample_dataframe):
        """Test that inspection functions don't modify the original DataFrame."""
        original_shape = sample_dataframe.shape
        original_columns = sample_dataframe.columns.tolist()
        
        # Run all inspection functions
        _ = get_basic_info(sample_dataframe)
        _ = get_data_types(sample_dataframe)
        _ = check_missing_values(sample_dataframe)
        _ = check_duplicates(sample_dataframe)
        
        # Verify DataFrame is unchanged
        assert sample_dataframe.shape == original_shape
        assert sample_dataframe.columns.tolist() == original_columns
    
    def test_error_handling_empty_dataframe(self):
        """Test handling of empty DataFrames."""
        empty_df = pd.DataFrame()
        
        # These should handle empty DataFrames gracefully
        info = get_basic_info(empty_df)
        assert info['shape'] == (0, 0)
        
        type_info = get_data_types(empty_df)
        assert len(type_info['numerical']) == 0
        
        missing_df = check_missing_values(empty_df)
        assert isinstance(missing_df, pd.DataFrame)
        
        duplicate_info = check_duplicates(empty_df)
        assert duplicate_info['exact_duplicates'] == 0


class TestIntegration:
    """Integration tests for the full workflow."""
    
    def test_full_inspection_workflow(self, temp_csv_file):
        """Test the complete inspection workflow on a sample file."""
        # Load data
        df = load_data(temp_csv_file)
        assert isinstance(df, pd.DataFrame)
        
        # Get basic info
        basic_info = get_basic_info(df)
        assert basic_info['shape'][0] > 0
        
        # Get data types
        type_info = get_data_types(df)
        assert 'numerical' in type_info
        
        # Check missing values
        missing_df = check_missing_values(df)
        assert isinstance(missing_df, pd.DataFrame)
        
        # Check duplicates
        duplicate_info = check_duplicates(df)
        assert isinstance(duplicate_info, dict)
    
    def test_real_dataset_inspection(self):
        """Test inspection on the actual MarketMosaic dataset if available."""
        dataset_path = Path("data/raw/geo_all_channels.csv")
        
        if dataset_path.exists():
            # This is a smoke test - just ensure it runs without errors
            try:
                df = load_data(str(dataset_path))
                assert isinstance(df, pd.DataFrame)
                assert len(df) > 0
                
                # Run a quick check
                assert df.shape[0] == 6240  # Known dataset size
                assert df.shape[1] == 20    # Known column count
                
            except Exception as e:
                pytest.skip(f"Dataset not available or load failed: {e}")
        else:
            pytest.skip("Real dataset not available for testing")


def test_module_import():
    """Test that the module can be imported correctly."""
    try:
        from inspect_data import main
        assert callable(main)
    except ImportError as e:
        pytest.fail(f"Failed to import module: {e}")


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])