import os
import pandas as pd

# Path definitions
RAW_CARS_PATH = os.path.join("data", "raw", "cars_2026.csv")
RAW_STATIONS_PATH = os.path.join("data", "raw", "charging_station.csv")

PROCESSED_CARS_PATH = os.path.join("data", "processed", "cleaned_cars_2026.csv")
PROCESSED_STATIONS_PATH = os.path.join("data", "processed", "cleaned_charging_station.csv")

def clean_cars_dataset(input_path, output_path):
    """
    Cleans the EV/cars dataset:
    - Strips whitespace from string columns
    - Removes duplicate rows
    - Converts date_reg to datetime
    - Drops rows with critical missing values (date_reg, fuel, state)
    - Saves clean output to CSV
    """
    print(f"Cleaning cars dataset: {input_path}")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Source file not found: {input_path}")

    # Load dataset
    df = pd.read_csv(input_path)
    initial_rows = len(df)

    # Strip whitespaces from string columns
    string_cols = df.select_dtypes(include=['object']).columns
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()

    # Drop rows with critical null fields
    df = df.dropna(subset=['date_reg', 'fuel', 'state'])
    
    # Filter strictly for electric vehicles (EVs)
    df['fuel'] = df['fuel'].astype(str).str.strip().str.lower()
    df = df[df['fuel'] == 'electric']
    
    # Drop duplicate rows
    df = df.drop_duplicates()
    
    # Parse date_reg to datetime
    df['date_reg'] = pd.to_datetime(df['date_reg'], errors='coerce')
    df = df.dropna(subset=['date_reg'])
    
    # Format date_reg to YYYY-MM-DD string representation
    df['date_reg'] = df['date_reg'].dt.strftime('%Y-%m-%d')

    # Save to destination
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    cleaned_rows = len(df)
    print(f"Cars dataset cleaned. Rows: {initial_rows} -> {cleaned_rows} (removed {initial_rows - cleaned_rows})")
    return df

def clean_charging_stations_dataset(input_path, output_path):
    """
    Cleans the charging stations dataset:
    - Strips whitespace from string columns
    - Removes duplicate rows
    - Filters records to only include Malaysia (country_code == 'MY')
    - Validates latitude and longitude (drops out of range or NaN coordinates)
    - Ensures ID is not null
    - Fills other missing columns with 'Unknown'
    - Saves clean output to CSV
    """
    print(f"Cleaning charging stations dataset: {input_path}")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Source file not found: {input_path}")

    # Load dataset
    df = pd.read_csv(input_path)
    initial_rows = len(df)

    # Strip whitespaces from string columns
    string_cols = df.select_dtypes(include=['object']).columns
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()

    # Ensure country_code is uppercase before dropping duplicates to handle case-variant duplicates
    if 'country_code' in df.columns:
        df['country_code'] = df['country_code'].astype(str).str.upper()

    # Drop duplicate rows
    df = df.drop_duplicates()

    # Filter for Malaysia (MY)
    df = df[df['country_code'] == 'MY']

    # Convert coordinates to numeric, coercion yields NaN on errors
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

    # Validate coordinate ranges
    df = df.dropna(subset=['latitude', 'longitude'])
    df = df[(df['latitude'] >= -90) & (df['latitude'] <= 90)]
    df = df[(df['longitude'] >= -180) & (df['longitude'] <= 180)]

    # Validate ID is present
    df = df.dropna(subset=['id'])

    # Standardize power_kw
    df['power_kw'] = pd.to_numeric(df['power_kw'], errors='coerce')

    # Fill empty text fields with 'Unknown'
    fill_unknown_cols = ['name', 'city', 'state_province', 'power_class']
    for col in fill_unknown_cols:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown').replace('', 'Unknown')

    # Save to destination
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    cleaned_rows = len(df)
    print(f"Charging stations cleaned. Rows: {initial_rows} -> {cleaned_rows} (removed {initial_rows - cleaned_rows})")
    return df

def main():
    try:
        clean_cars_dataset(RAW_CARS_PATH, PROCESSED_CARS_PATH)
        clean_charging_stations_dataset(RAW_STATIONS_PATH, PROCESSED_STATIONS_PATH)
        print("Data cleaning completed successfully.")
    except Exception as e:
        print(f"Error during data cleaning execution: {e}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()
