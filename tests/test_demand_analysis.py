import os
import pandas as pd
import pytest
from src.demand_analysis import (
    CLEANED_CARS_PATH,
    load_data,
    filter_ev_records,
    calculate_ev_distribution
)

def test_filter_ev_records():
    """Verify that electric and hybrid records are retained."""
    mock_data = pd.DataFrame({
        'fuel': ['electric', 'petrol', 'hybrid_petrol', 'diesel', ' hybrid_diesel '],
        'state': ['Johor', 'Selangor', 'Sabah', 'KL', 'Penang']
    })
    
    ev_df = filter_ev_records(mock_data)
    assert len(ev_df) == 3
    # Check that electric and hybrid, trimmed / case-insensitive inputs are correctly handled
    assert set(ev_df['state']) == {'Johor', 'Sabah', 'Penang'}

def test_calculate_ev_distribution():
    """Verify state adoption grouping counts and descending ordering."""
    mock_ev_data = pd.DataFrame({
        'fuel': ['electric', 'electric', 'electric', 'electric'],
        'state': ['Selangor', 'Johor', 'Selangor', 'Perak']
    })
    
    dist_df = calculate_ev_distribution(mock_ev_data)
    assert len(dist_df) == 3
    
    # Check order (highest count first)
    assert dist_df.iloc[0]['state'] == 'Selangor'
    assert dist_df.iloc[0]['ev_count'] == 2
    
    assert dist_df.iloc[1]['state'] in ['Johor', 'Perak']
    assert dist_df.iloc[1]['ev_count'] == 1

def test_actual_cleaned_data_ev_distribution():
    """Verify load and calculation succeeds on the actual cleaned dataset."""
    if not os.path.exists(CLEANED_CARS_PATH):
        pytest.skip(f"Cleaned cars file {CLEANED_CARS_PATH} does not exist. Skipping actual data test.")
        
    df = load_data(CLEANED_CARS_PATH)
    ev_df = filter_ev_records(df)
    dist_df = calculate_ev_distribution(ev_df)
    
    # Assertions on actual cleaned data
    assert len(ev_df) > 0, "No EV records found in actual cleaned dataset"
    assert len(dist_df) > 0, "Distribution DataFrame is empty"
    assert 'state' in dist_df.columns
    assert 'ev_count' in dist_df.columns
    # Ensure it's sorted descending
    assert dist_df['ev_count'].is_monotonic_decreasing
