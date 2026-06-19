# Project Instructions

Project: Electric Vehicle (EV) Charging Station Demand & Grid Load Planner
Theme: Green Community Transition

This document explains the recommended project structure, branch strategy, development flow, and deployment plan for the Agile MVP.

---

## 1. Project Overview

The EV Charging Station Demand & Grid Load Planner is a data science application concept that analyzes EV adoption, charging station availability, and possible grid load risk.

The purpose of this project is to support data-driven planning for EV infrastructure in Malaysia. The MVP focuses on early usable outputs such as cleaned datasets, demand summary tables, EV-to-charger ratio analysis, grid load simulation, and a Streamlit dashboard prototype.

The project uses:

* Python for data processing and analysis.
* Streamlit for dashboard prototype.
* GitHub for version control.
* GitHub Actions for CI/CD checks.
* Railway for planned dashboard deployment.

---

## 2. Recommended Project Structure

```text
ev-charging-demand-planner/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   │   ├── cars_2026.csv
│   │   └── charging_station.csv
│   │
│   └── processed/
│       ├── cleaned_cars_2026.csv
│       ├── cleaned_charging_station.csv
│       ├── ev_charger_ratio.csv
│       └── grid_load_simulation.csv
│
├── docs/
│   ├── user_story.md
│   └── instruction.md
│
├── notebooks/
│   └── exploratory_analysis.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data_cleaning.py
│   ├── demand_analysis.py
│   ├── load_simulation.py
│   └── utils.py
│
├── tests/
│   ├── test_data_cleaning.py
│   ├── test_demand_analysis.py
│   └── test_load_simulation.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
├── README.md
├── requirements.txt
└── Procfile
```

---

## 3. Folder Purpose

### `app/`

Contains the Streamlit dashboard application.

Main file:

```text
app/streamlit_app.py
```

This file is used to display the EV demand analysis, charging station summary, EV-to-charger ratio, and grid load simulation output.

---

### `data/raw/`

Stores the original datasets.

Example:

```text
data/raw/cars_2026.csv
data/raw/charging_station.csv
```

Raw files should not be edited directly.

---

### `data/processed/`

Stores cleaned and generated output files.

Example:

```text
data/processed/cleaned_cars_2026.csv
data/processed/cleaned_charging_station.csv
data/processed/ev_charger_ratio.csv
data/processed/grid_load_simulation.csv
```

These files are produced after data cleaning, demand analysis, and load simulation.

---

### `docs/`

Stores project documentation.

Example:

```text
docs/user_story.md
docs/instruction.md
```

---

### `notebooks/`

Stores exploratory analysis notebooks.

Example:

```text
notebooks/exploratory_analysis.ipynb
```

Use this folder for checking dataset structure, missing values, charts, and early analysis.

---

### `src/`

Stores reusable Python scripts.

Suggested files:

```text
src/data_cleaning.py
src/demand_analysis.py
src/load_simulation.py
src/utils.py
```

Purpose:

* `data_cleaning.py`: clean EV and charging station datasets.
* `demand_analysis.py`: calculate EV distribution and EV-to-charger ratio.
* `load_simulation.py`: estimate grid load and assign risk level.
* `utils.py`: shared helper functions.

---

### `tests/`

Stores basic test files.

Example:

```text
tests/test_data_cleaning.py
tests/test_demand_analysis.py
tests/test_load_simulation.py
```

Tests are used by GitHub Actions to check whether the main scripts run correctly.

---

### `.github/workflows/`

Stores GitHub Actions CI/CD workflow.

Example:

```text
.github/workflows/ci.yml
```

The workflow can check:

* Python installation.
* Package installation from `requirements.txt`.
* Basic test execution.
* Streamlit app file existence.

---

## 4. Branch Strategy

This project uses three main branches:

```text
main
release
dev
```

---

### `main` Branch

Purpose:

The `main` branch stores the final stable version of the project.

Rules:

* Only final and approved work should be merged into `main`.
* This branch represents the version used for final submission.
* No direct development should be done in `main`.

Used for:

* Final project version.
* Final slide screenshots.
* Final presentation demo reference.

---

### `release` Branch

Purpose:

The `release` branch stores the version prepared for deployment or final testing.

Rules:

* Merge from `dev` into `release` after sprint work is completed.
* Test the dashboard and documentation in this branch.
* Fix small issues before merging into `main`.

Used for:

* Final testing.
* Railway deployment preparation.
* Checking README, dashboard, and processed outputs.

---

### `dev` Branch

Purpose:

The `dev` branch is used for active development.

Rules:

* Most development work starts from `dev`.
* New scripts, dashboard updates, and analysis changes are added here first.
* After testing, changes can be merged into `release`.

Used for:

* Sprint development.
* Data cleaning updates.
* Analysis scripts.
* Dashboard prototype changes.

---

## 5. Recommended Development Flow

### Step 1: Start from `dev`

Create or switch to the `dev` branch.

```bash
git checkout -b dev
```

Use this branch for normal development work.

---

### Step 2: Commit Sprint Tasks

After completing a task, commit the change clearly.

Example:

```bash
git add .
git commit -m "Sprint 1: add project structure and requirements file"
```

---

### Step 3: Push to GitHub

Push changes to GitHub.

```bash
git push origin dev
```

---

### Step 4: Merge `dev` into `release`

After sprint work is tested, merge into `release`.

```bash
git checkout release
git merge dev
git push origin release
```

---

### Step 5: Test Release Version

Check that the project works properly from the `release` branch.

Suggested checks:

* Dashboard can run locally.
* README is updated.
* Processed files are available.
* GitHub Actions checks pass.

---

### Step 6: Merge `release` into `main`

After final checking, merge the approved version into `main`.

```bash
git checkout main
git merge release
git push origin main
```

---

## 6. GitHub Actions CI/CD Plan

GitHub Actions will be used to support CI/CD by automatically checking the project whenever changes are pushed.

Suggested checks:

* Install Python.
* Install packages from `requirements.txt`.
* Run basic tests.
* Confirm that `app/streamlit_app.py` exists.

Example workflow file:

```yaml
name: CI Check

on:
  push:
    branches:
      - dev
      - release
      - main
  pull_request:
    branches:
      - release
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Check Streamlit app file
        run: |
          test -f app/streamlit_app.py

      - name: Run tests
        run: |
          pytest
```

---

## 7. Railway Deployment Plan

The project dashboard can be deployed using Railway.

### Deployment Steps

1. Push the final project to GitHub.
2. Log in to Railway.
3. Create a new Railway project.
4. Connect the GitHub repository.
5. Select the branch for deployment, preferably `release`.
6. Add the Streamlit start command.
7. Railway installs packages from `requirements.txt`.
8. Railway generates the dashboard application URL.

---

## 8. Railway Start Command

Use this command to run the Streamlit dashboard on Railway:

```bash
streamlit run app/streamlit_app.py --server.port $PORT --server.address 0.0.0.0
```

This command can be placed in a `Procfile`.

Example `Procfile`:

```text
web: streamlit run app/streamlit_app.py --server.port $PORT --server.address 0.0.0.0
```

---

## 9. Suggested Requirements File

Example `requirements.txt`:

```text
pandas
numpy
streamlit
plotly
pytest
```

Add more packages only if they are used in the project.

---

## 10. Local Run Instructions

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit dashboard:

```bash
streamlit run app/streamlit_app.py
```

Run tests:

```bash
pytest
```

---

## 11. Agile Development Notes

This project follows Agile principles by improving the MVP across four sprints.

| Sprint   | Focus                                        | Output                                         |
| -------- | -------------------------------------------- | ---------------------------------------------- |
| Sprint 1 | Project setup and data preparation           | Cleaned dataset and project structure          |
| Sprint 2 | EV demand and infrastructure gap analysis    | EV-to-charger ratio and exploratory charts     |
| Sprint 3 | Grid load simulation and dashboard prototype | Load-risk simulation and Streamlit prototype   |
| Sprint 4 | MVP refinement and deployment planning       | Improved dashboard and Railway deployment plan |

The MVP starts as a cleaned dataset, then improves into analysis tables, then a dashboard prototype, and finally a refined dashboard with deployment planning.
