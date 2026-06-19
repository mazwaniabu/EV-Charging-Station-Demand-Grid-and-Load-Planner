import os
import pandas as pd
import pytest
from src.data_cleaning import (
    PROCESSED_CARS_PATH,
    PROCESSED_STATIONS_PATH,
    clean_cars_dataset,
    clean_charging_stations_dataset
)

def test_data_cleaning_execution(tmp_path):
    """
    Test that cleaning functions run successfully on test files and generate valid outputs.
    """
    # Create simple mock raw data for cars
    mock_cars_data = pd.DataFrame({
        'date_reg': ['2026-01-01', ' 2026-01-02 ', 'invalid-date', '2026-01-03', '2026-01-01'],
        'type': ['motokar', 'jip', 'motokar', 'motokar', 'motokar'],
        'maker': ['BMW', 'Chery', 'BMW', 'BMW', 'BMW'],
        'model': ['7 Series', 'Tiggo', '7 Series', '7 Series', '7 Series'],
        'colour': ['black', 'grey', 'black', 'black', 'black'],
        'fuel': ['electric', 'hybrid_petrol', 'electric', 'petrol', 'electric'],
        'state': ['Johor', 'Selangor', 'Johor', 'Johor', 'Johor']
    })
    
    mock_cars_file = tmp_path / "mock_cars.csv"
    mock_cars_data.to_csv(mock_cars_file, index=False)
    
    output_cars_file = tmp_path / "cleaned_mock_cars.csv"
    
    # Run cleaner
    cleaned_cars_df = clean_cars_dataset(str(mock_cars_file), str(output_cars_file))
    
    # Verify outputs
    assert os.path.exists(output_cars_file)
    assert len(cleaned_cars_df) == 2  # Dupes, invalid date, and non-EV/hybrid rows removed
    assert cleaned_cars_df['fuel'].isin(['electric', 'hybrid_petrol', 'hybrid_diesel']).all()
    assert (cleaned_cars_df['date_reg'] == '2026-01-02').any()
    
    # Create simple mock raw data for charging stations
    mock_stations_data = pd.DataFrame({
        'id': [307660, 307660, 301207, 301208],
        'name': ['Station A', 'Station A', 'Station B', 'Station C'],
        'city': ['Kuala Lumpur', 'Kuala Lumpur', 'Andorra', 'Penang'],
        'state_province': ['KL', 'KL', 'UNKNOWN', 'Penang'],
        'country_code': ['MY', 'my', 'AD', 'MY'],
        'latitude': [3.139, 3.139, 42.505, 999.0],  # 999 is invalid latitude
        'longitude': [101.686, 101.686, 1.528, 101.5],
        'ports': [4, 4, 10, 2],
        'power_kw': [22.0, 22.0, 300.0, 50.0],
        'power_class': ['AC', 'AC', 'DC', 'DC'],
        'is_fast_dc': [False, False, True, True]
    })
    
    mock_stations_file = tmp_path / "mock_stations.csv"
    mock_stations_data.to_csv(mock_stations_file, index=False)
    
    output_stations_file = tmp_path / "cleaned_mock_stations.csv"
    
    # Run cleaner
    cleaned_stations_df = clean_charging_stations_dataset(str(mock_stations_file), str(output_stations_file))
    
    # Verify outputs
    assert os.path.exists(output_stations_file)
    assert len(cleaned_stations_df) == 1  # Dupes removed, Andorra (AD) removed, 999.0 latitude removed
    assert cleaned_stations_df.iloc[0]['name'] == 'Station A'
    assert cleaned_stations_df.iloc[0]['country_code'] == 'MY'


def test_processed_files_exist_and_are_valid():
    """
    Test that actual cleaned files exist and satisfy schema/values constraints.
    (This test assumes the clean_data script has been executed on raw datasets).
    """
    # Check if cleaned files exist
    if not (os.path.exists(PROCESSED_CARS_PATH) and os.path.exists(PROCESSED_STATIONS_PATH)):
        pytest.skip("Cleaned files do not exist yet. Skip validation.")
        
    # Read actual files
    cars_df = pd.read_csv(PROCESSED_CARS_PATH)
    stations_df = pd.read_csv(PROCESSED_STATIONS_PATH)
    
    # Validate cars
    assert not cars_df.duplicated().any(), "Cleaned cars file contains duplicates"
    assert not cars_df['date_reg'].isnull().any(), "Cleaned cars contain null date_reg values"
    assert cars_df['fuel'].isin(['electric', 'hybrid_petrol', 'hybrid_diesel']).all(), "Cleaned cars contains non-EV/hybrid records"
    
    # Validate stations
    assert not stations_df.duplicated().any(), "Cleaned stations file contains duplicates"
    assert (stations_df['country_code'] == 'MY').all(), "Cleaned stations file contains non-MY entries"
    assert (stations_df['latitude'] >= -90).all() and (stations_df['latitude'] <= 90).all(), "Invalid latitude"
    assert (stations_df['longitude'] >= -180).all() and (stations_df['longitude'] <= 180).all(), "Invalid longitude"
