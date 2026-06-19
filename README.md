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
