import os
import pandas as pd

# Path to the cleaned cars dataset
CLEANED_CARS_PATH = os.path.join("data", "processed", "cleaned_cars_2026.csv")

def load_data(file_path):
    """Loads a CSV file into a pandas DataFrame."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)

def filter_ev_records(df):
    """Filters the input DataFrame to only keep records where fuel is 'electric'."""
    if 'fuel' not in df.columns:
        raise ValueError("Input DataFrame is missing required 'fuel' column")
    
    # Filter for electric vehicles (case-insensitive strip just in case)
    ev_df = df[df['fuel'].astype(str).str.strip().str.lower() == 'electric'].copy()
    return ev_df

def calculate_ev_distribution(df):
    """
    Groups the EV records by state and counts them.
    Returns a DataFrame with columns ['state', 'ev_count'] sorted descending.
    """
    if 'state' not in df.columns:
        raise ValueError("Input DataFrame is missing required 'state' column")
        
    dist_df = df.groupby('state').size().reset_index(name='ev_count')
    dist_df = dist_df.sort_values(by='ev_count', ascending=False).reset_index(drop=True)
    return dist_df

def main():
    try:
        print(f"Loading cleaned dataset from {CLEANED_CARS_PATH}...")
        df = load_data(CLEANED_CARS_PATH)
        
        print("Filtering for EV records...")
        ev_df = filter_ev_records(df)
        total_evs = len(ev_df)
        print(f"Total EVs found: {total_evs} (out of {len(df)} total registered vehicles)")
        
        print("Calculating EV distribution by state...")
        dist_df = calculate_ev_distribution(ev_df)
        
        print("\n--- EV Distribution in Malaysia ---")
        print(dist_df.to_string(index=False))
        
    except Exception as e:
        print(f"Error executing EV analysis: {e}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()
