import pytest
import pandas as pd
import numpy as np
from src.load_simulation import (
    map_capacity_rating,
    calculate_coincidence_factor,
    classify_grid_risk,
    run_simulation
)

def test_map_capacity_rating_valid():
    # Valid numeric input should be returned directly
    assert map_capacity_rating(45.0, 'AC_L2_(7.5-21kW)', False) == 45.0
    assert map_capacity_rating(120, 'UNKNOWN', True) == 120.0

def test_map_capacity_rating_by_class():
    # Null or invalid numeric input should map based on class
    assert map_capacity_rating(np.nan, 'AC_L1_(<7.5kW)', False) == 3.7
    assert map_capacity_rating(None, 'AC_L2_(7.5-21kW)', False) == 11.0
    assert map_capacity_rating(0.0, 'AC_HIGH_(22-49kW)', False) == 22.0
    assert map_capacity_rating(-5.0, 'DC_FAST_(50-149kW)', True) == 50.0
    assert map_capacity_rating(np.nan, 'DC_ULTRA_(>=150kW)', True) == 150.0

def test_map_capacity_rating_fallback():
    # UNKNOWN class should fallback to is_fast_dc
    assert map_capacity_rating(np.nan, 'UNKNOWN', True) == 50.0
    assert map_capacity_rating(np.nan, 'UNKNOWN', False) == 11.0
    assert map_capacity_rating(None, None, True) == 50.0
    assert map_capacity_rating(None, None, False) == 11.0

def test_calculate_coincidence_factor():
    # Test boundary/invalid inputs
    assert calculate_coincidence_factor(0) == 1.0
    assert calculate_coincidence_factor(-1) == 1.0
    assert calculate_coincidence_factor(None) == 1.0
    
    # Test specific values
    # For N = 1, CF = 0.20 + 0.80 * 1.0 = 1.0
    assert pytest.approx(calculate_coincidence_factor(1, 0.20)) == 1.0
    # For N = 4, CF = 0.20 + 0.80 * 0.5 = 0.60
    assert pytest.approx(calculate_coincidence_factor(4, 0.20)) == 0.60
    # For N = 100, CF = 0.20 + 0.80 * 0.10 = 0.28
    assert pytest.approx(calculate_coincidence_factor(100, 0.20)) == 0.28

def test_classify_grid_risk():
    # Low threshold < 500, High threshold >= 1500
    assert classify_grid_risk(100) == 'Low'
    assert classify_grid_risk(499.9) == 'Low'
    assert classify_grid_risk(500) == 'Medium'
    assert classify_grid_risk(1499) == 'Medium'
    assert classify_grid_risk(1500) == 'High'
    assert classify_grid_risk(2500) == 'High'
    
    # Custom thresholds
    assert classify_grid_risk(100, 200, 400) == 'Low'
    assert classify_grid_risk(250, 200, 400) == 'Medium'
    assert classify_grid_risk(450, 200, 400) == 'High'

def test_run_simulation_aggregate():
    # Create mock dataset
    data = {
        'id': [1, 2, 3, 4],
        'name': ['S1', 'S2', 'S3', 'S4'],
        'city': ['KL', 'KL', 'JB', 'JB'],
        'state_province': ['Kuala Lumpur', 'Kuala Lumpur', 'Johor', 'Johor'],
        'country_code': ['MY', 'MY', 'MY', 'MY'],
        'latitude': [3.1, 3.2, 1.5, 1.6],
        'longitude': [101.6, 101.7, 103.7, 103.8],
        'ports': [2, 2, 4, 4],
        'power_kw': [22.0, np.nan, 50.0, 50.0],
        'power_class': ['AC_HIGH_(22-49kW)', 'AC_L2_(7.5-21kW)', 'DC_FAST_(50-149kW)', 'DC_FAST_(50-149kW)'],
        'is_fast_dc': [False, False, True, True]
    }
    df = pd.DataFrame(data)
    
    # Run simulation with default cf_min=0.2
    # KL: Total stations=2, Ports=4, Capacity = 22.0 + 11.0 (imputed) = 33.0 kW
    # CF for 4 ports = 0.20 + 0.80 * 0.50 = 0.60
    # Peak load for KL = 33.0 * 0.60 = 19.8 kW (Risk: Low since < 500)
    #
    # Johor: Total stations=2, Ports=8, Capacity = 50.0 + 50.0 = 100.0 kW
    # CF for 8 ports = 0.20 + 0.80 * (8 ** -0.5) = 0.20 + 0.80 * 0.35355 = 0.4828
    # Peak load for Johor = 100.0 * 0.4828 = 48.28 kW (Risk: Low since < 500)
    
    sim_df = run_simulation(df, cf_min=0.20, low_threshold=30.0, high_threshold=45.0)
    
    assert len(sim_df) == 2
    
    # Johor has higher peak load (48.28 kW) than KL (19.8 kW), so it should be first
    assert sim_df.iloc[0]['state_province'] == 'Johor'
    assert sim_df.iloc[0]['total_stations'] == 2
    assert sim_df.iloc[0]['total_ports'] == 8
    assert sim_df.iloc[0]['installed_capacity_kw'] == 100.0
    assert pytest.approx(sim_df.iloc[0]['coincident_peak_load_kw'], 0.1) == 48.3
    assert sim_df.iloc[0]['grid_risk_level'] == 'High' # > 45
    
    assert sim_df.iloc[1]['state_province'] == 'Kuala Lumpur'
    assert sim_df.iloc[1]['total_stations'] == 2
    assert sim_df.iloc[1]['total_ports'] == 4
    assert sim_df.iloc[1]['installed_capacity_kw'] == 33.0
    assert pytest.approx(sim_df.iloc[1]['coincident_peak_load_kw'], 0.1) == 19.8
    assert sim_df.iloc[1]['grid_risk_level'] == 'Low' # < 30
