# EV Charging Station Demand & Grid Load Planner

A data science application designed to analyze EV adoption, charging station availability, and potential utility grid load risk in Malaysia. This project is developed as part of the Green Community Transition theme.

## Project Structure

```text
ev-charging-demand-planner/
│
├── app/                  # Streamlit dashboard application
│   └── streamlit_app.py
│
├── data/                 # Datasets
│   ├── raw/              # Original, unmodified datasets (cars_2026.csv, charging_station.csv)
│   └── processed/        # Cleaned and simulated output files
│
├── docs/                 # Documentation (user stories, instructions)
│   ├── user_story.md
│   └── instruction.md
│
├── notebooks/            # Exploratory data analysis notebooks
│   └── exploratory_analysis.ipynb
│
├── src/                  # Reusable Python logic/scripts
│   ├── __init__.py
│   ├── data_cleaning.py
│   ├── demand_analysis.py
│   ├── load_simulation.py
│   └── utils.py
│
├── tests/                # Unit tests for core scripts
│   ├── test_data_cleaning.py
│   ├── test_demand_analysis.py
│   └── test_load_simulation.py
│
├── .github/              # GitHub CI/CD configuration
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
├── requirements.txt
└── Procfile
```

## Branch Strategy

- **`main`**: The final stable and approved version of the project.
- **`release`**: Version prepared for final testing and Railway deployment.
- **`dev`**: Active development branch where sprint tasks are implemented.

## Local Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run tests**:
   ```bash
   pytest
   ```

3. **Run Streamlit app locally**:
   ```bash
   streamlit run app/streamlit_app.py
   ```

## Grid Load Simulation Model

The planner implements a **Coincident Peak Load Simulation Engine** (found in `src/load_simulation.py`) to model the peak load stress of EV chargers on the utility grid for each state.

- **Coincidence Factor ($CF$):** Estimates the probability of multiple chargers active at peak power simultaneously. It decreases non-linearly as the number of ports ($N$) in a state increases:
  $$CF(N) = CF_{min} + (1 - CF_{min}) \times N^{-0.5}$$
  Where $CF_{min}$ (default `0.20`, adjustable in the dashboard) represents the baseline minimum coincidence factor for massive networks.
- **Coincident Peak Load:** Sum of all stations' power capacity in the state multiplied by the coincidence factor:
  $$\text{Peak Load} = \text{Installed Capacity} \times CF(N)$$
- **Risk Classification:**
  - 🟢 **Low Risk**: Peak Load < 500 kW
  - 🟡 **Medium Risk**: 500 kW <= Peak Load < 1,500 kW
  - 🔴 **High Risk**: Peak Load >= 1,500 kW

## Deployment Configuration

This project is configured for production hosting (e.g. on Railway) using:
- **`Procfile`**: Specifies the startup server command binding the app to the dynamic port allocation `$PORT`:
  ```text
  web: streamlit run app/streamlit_app.py --server.port $PORT --server.address 0.0.0.0
  ```
- **`requirements.txt`**: Standardized, deterministic dependencies ensuring stable production build runs.

