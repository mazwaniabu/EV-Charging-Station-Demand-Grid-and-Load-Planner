import os
import csv
import sys

# Define relative paths to data files
CARS_CSV_PATH = os.path.join("data", "raw", "cars_2026.csv")
CHARGING_STATION_CSV_PATH = os.path.join("data", "raw", "charging_station.csv")

# Expected schemas
EXPECTED_CARS_COLUMNS = ['date_reg', 'type', 'maker', 'model', 'colour', 'fuel', 'state']
EXPECTED_CHARGING_STATION_COLUMNS = [
    'id', 'name', 'city', 'state_province', 'country_code',
    'latitude', 'longitude', 'ports', 'power_kw', 'power_class', 'is_fast_dc'
]

def verify_csv_schema(file_path, expected_columns):
    """
    Verifies that the CSV file exists, has a valid header matching expected columns, 
    and contains at least one row of data.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return False, 0

    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            
            if not header:
                print(f"Error: File '{file_path}' is empty or has no header.")
                return False, 0
                
            # Verify columns match exactly
            if header != expected_columns:
                print(f"Error: Schema mismatch for '{file_path}'.")
                print(f"  Expected: {expected_columns}")
                print(f"  Found:    {header}")
                return False, 0
                
            # Count rows to ensure it contains data
            row_count = sum(1 for _ in reader)
            return True, row_count
            
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return False, 0

def main():
    print("Verifying raw datasets structure...")
    
    cars_ok, cars_count = verify_csv_schema(CARS_CSV_PATH, EXPECTED_CARS_COLUMNS)
    stations_ok, stations_count = verify_csv_schema(CHARGING_STATION_CSV_PATH, EXPECTED_CHARGING_STATION_COLUMNS)
    
    if cars_ok:
        print(f"✓ '{CARS_CSV_PATH}' is valid. Found {cars_count} records.")
    else:
        print(f"✗ '{CARS_CSV_PATH}' validation failed.")
        
    if stations_ok:
        print(f"✓ '{CHARGING_STATION_CSV_PATH}' is valid. Found {stations_count} records.")
    else:
        print(f"✗ '{CHARGING_STATION_CSV_PATH}' validation failed.")
        
    if not (cars_ok and stations_ok):
        sys.exit(1)
        
    print("All raw datasets verified successfully!")
    sys.exit(0)

if __name__ == "__main__":
    main()
