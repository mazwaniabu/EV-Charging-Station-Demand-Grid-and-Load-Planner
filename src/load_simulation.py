import os
import sys
import pandas as pd
import numpy as np

# Ensure root directory is in the path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

# Path definitions
INPUT_STATIONS_PATH = os.path.join("data", "processed", "cleaned_charging_station.csv")
OUTPUT_SIMULATION_PATH = os.path.join("data", "processed", "grid_load_simulation.csv")

def map_capacity_rating(power_kw, power_class, is_fast_dc):
    """
    Imputes missing capacity ratings (power_kw) based on power_class and charger type.
    """
    if pd.notna(power_kw) and power_kw > 0:
        return float(power_kw)
    
    # Map based on power_class string
    power_class_str = str(power_class).strip() if pd.notna(power_class) else 'UNKNOWN'
    
    mapping = {
        'AC_L1_(<7.5kW)': 3.7,
        'AC_L2_(7.5-21kW)': 11.0,
        'AC_HIGH_(22-49kW)': 22.0,
        'DC_FAST_(50-149kW)': 50.0,
        'DC_ULTRA_(>=150kW)': 150.0
    }
    
    if power_class_str in mapping:
        return mapping[power_class_str]
    
    # Fallback to is_fast_dc
    if is_fast_dc is True or str(is_fast_dc).lower() == 'true':
        return 50.0
    else:
        return 11.0

def calculate_coincidence_factor(num_ports, cf_min=0.20):
    """
    Calculates the coincidence factor for a given number of ports.
    Formula: CF = cf_min + (1 - cf_min) * (num_ports ** -0.5)
    """
    if pd.isna(num_ports) or num_ports <= 0:
        return 1.0
    
    cf = cf_min + (1 - cf_min) * (num_ports ** -0.5)
    return float(min(1.0, max(0.0, cf)))

def classify_grid_risk(peak_load_kw, low_threshold=500.0, high_threshold=1500.0):
    """
    Classifies grid load risk level as Low, Medium, or High based on coincident peak load.
    """
    if pd.isna(peak_load_kw):
        return 'Low'
    if peak_load_kw < low_threshold:
        return 'Low'
    elif peak_load_kw < high_threshold:
        return 'Medium'
    else:
        return 'High'

def run_simulation(stations_df, cf_min=0.20, low_threshold=500.0, high_threshold=1500.0):
    """
    Executes the grid load simulation on the charging stations DataFrame.
    """
    df = stations_df.copy()
    
    # 1. Standardize and default critical columns
    df['ports'] = pd.to_numeric(df['ports'], errors='coerce').fillna(1).astype(int)
    df['ports'] = df['ports'].apply(lambda x: x if x > 0 else 1)
    
    # 2. Map capacity ratings
    df['power_kw'] = df.apply(
        lambda r: map_capacity_rating(r.get('power_kw'), r.get('power_class'), r.get('is_fast_dc')),
        axis=1
    )
    
    # 3. Aggregate by state
    state_groups = df.groupby('state_province')
    
    sim_rows = []
    for state, group in state_groups:
        total_stations = len(group)
        total_ports = int(group['ports'].sum())
        installed_capacity_kw = float(group['power_kw'].sum())
        
        # Calculate state-level coincidence factor
        cf = calculate_coincidence_factor(total_ports, cf_min)
        
        # Calculate coincident peak load
        coincident_peak_load_kw = installed_capacity_kw * cf
        
        # Classify risk
        risk_level = classify_grid_risk(coincident_peak_load_kw, low_threshold, high_threshold)
        
        sim_rows.append({
            'state_province': state,
            'total_stations': total_stations,
            'total_ports': total_ports,
            'installed_capacity_kw': round(installed_capacity_kw, 2),
            'coincidence_factor': round(cf, 4),
            'coincident_peak_load_kw': round(coincident_peak_load_kw, 2),
            'grid_risk_level': risk_level
        })
        
    sim_df = pd.DataFrame(sim_rows)
    # Sort descending by coincident peak load
    if not sim_df.empty:
        sim_df = sim_df.sort_values(by='coincident_peak_load_kw', ascending=False).reset_index(drop=True)
    return sim_df

def main():
    print(f"Running peak grid load simulation using: {INPUT_STATIONS_PATH}")
    if not os.path.exists(INPUT_STATIONS_PATH):
        print(f"Error: Input file does not exist: {INPUT_STATIONS_PATH}")
        sys.exit(1)
        
    stations_df = pd.read_csv(INPUT_STATIONS_PATH)
    sim_df = run_simulation(stations_df)
    
    os.makedirs(os.path.dirname(OUTPUT_SIMULATION_PATH), exist_ok=True)
    sim_df.to_csv(OUTPUT_SIMULATION_PATH, index=False)
    print(f"Simulation completed. Output saved to: {OUTPUT_SIMULATION_PATH}")
    print("\nSimulation Results summary:")
    print(sim_df)

if __name__ == "__main__":
    main()
