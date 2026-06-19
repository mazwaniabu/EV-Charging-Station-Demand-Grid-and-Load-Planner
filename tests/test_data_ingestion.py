import os
import csv
import pytest
from src.verify_raw_data import (
    CARS_CSV_PATH,
    CHARGING_STATION_CSV_PATH,
    EXPECTED_CARS_COLUMNS,
    EXPECTED_CHARGING_STATION_COLUMNS,
    verify_csv_schema
)

def test_cars_dataset_schema():
    """
    Test that the cars_2026.csv file exists, matches the expected schema, and contains records.
    """
    assert os.path.exists(CARS_CSV_PATH), f"{CARS_CSV_PATH} does not exist"
    
    is_valid, count = verify_csv_schema(CARS_CSV_PATH, EXPECTED_CARS_COLUMNS)
    assert is_valid, "cars_2026.csv failed schema validation"
    assert count > 0, "cars_2026.csv is empty (contains no records)"

def test_charging_stations_dataset_schema():
    """
    Test that the charging_station.csv file exists, matches the expected schema, and contains records.
    """
    assert os.path.exists(CHARGING_STATION_CSV_PATH), f"{CHARGING_STATION_CSV_PATH} does not exist"
    
    is_valid, count = verify_csv_schema(CHARGING_STATION_CSV_PATH, EXPECTED_CHARGING_STATION_COLUMNS)
    assert is_valid, "charging_station.csv failed schema validation"
    assert count > 0, "charging_station.csv is empty (contains no records)"
