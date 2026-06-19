# User Stories and Sprint Tasks

Project: Electric Vehicle (EV) Charging Station Demand & Grid Load Planner
Theme: Green Community Transition

This document describes the user stories, acceptance criteria, and sprint tasks for the Agile MVP development plan.

---

## Sprint 1 - Project Setup and Data Preparation

### User Story 1: EV Charging Demand Identification

**Description:**
As a Charging Point Operator, I want to identify areas with high EV adoption but limited charging stations so that I can plan new charging infrastructure more effectively.

### Acceptance Criteria

* GitHub repository is initialized.
* Project folder structure is created.
* Required Python dependencies are listed in `requirements.txt`.
* EV dataset and charging station dataset are uploaded and verified.
* Raw data structure and column names are checked.
* EV and charging station datasets are cleaned.
* Basic GitHub Actions workflow is created for dependency checking.

### Tasks

* `[Environment Setup]` Initialize Git repository and structure project directory.
* `[Dependency Management]` Create a `requirements.txt` manifest specifying required packages.
* `[Data Ingestion Hook]` Upload and verify raw file structures for `cars_2026.csv` and `charging_station.csv`.
* `[Data]` Clean EV and charging station dataset.
* `[CI/CD]` Set up basic GitHub Actions workflow for dependency checking.

### Sprint 1 MVP Output

Cleaned dataset and basic project environment ready for analysis.

---

## Sprint 2 - EV Demand and Infrastructure Gap Analysis

### User Story 1: EV Charging Demand Identification

**Description:**
As a Charging Point Operator, I want to identify areas with high EV adoption but limited charging stations so that I can plan new charging infrastructure more effectively.

### Acceptance Criteria

* EV records are extracted and filtered from `cars_2026.csv`.
* Charging station coordinates and location fields are processed.
* EV distribution by location can be summarized.
* Charging station distribution by location can be summarized.
* EV-to-charger ratio is calculated.
* Basic exploratory charts are created.

### Tasks

* EV Distribution & Density Analytics.
* Extract and filter EV records from `cars_2026.csv`.
* Process and validate coordinates in `charging_station.csv`.
* Calculate EV-to-charger ratio by location.
* Identify areas with possible charging infrastructure gaps.
* Create basic exploratory charts.

### Sprint 2 MVP Output

Initial EV demand and infrastructure gap analysis showing areas with high EV demand and limited charging availability.

---

## Sprint 3 - Grid Load Simulation and Dashboard Prototype

### User Story 2: Utility Grid Load Simulation

**Description:**
As a grid operator, I want to estimate possible charging load based on charger capacity so that I can identify locations that may create grid stress during peak demand.

### Acceptance Criteria

* AC/DC charger capacity is mapped to charging station records.
* Estimated peak charging load is calculated.
* Charging load risk is classified as Low, Medium, or High.
* Simulation output is shown in table or chart form.
* Initial Streamlit dashboard prototype is created and can run locally.

### Tasks

* Coincident Grid Load Simulation Engine.
* Map capacity ratings, such as AC/DC kW, to station records.
* Formulate and execute peak power simulation script.
* Create Low, Medium, and High load-risk classification.
* Construct interactive Streamlit dashboard interface.
* Add EV distribution, charger distribution, and load-risk output to dashboard.
* Test dashboard locally.

### Sprint 3 MVP Output

Dashboard prototype showing EV demand, charging station availability, and estimated grid load risk.

---

## Sprint 4 - MVP Refinement and Deployment

### User Story 3: Dashboard and Deployment

**Description:**
As a local council planner, I want to view EV charging demand and grid load insights through a simple dashboard so that planning decisions can be supported by clear visual evidence.

### Acceptance Criteria

* Dashboard layout is improved based on feedback.
* Chart labels and table formatting are clearer.
* Risk category explanation is added.
* GitHub Actions workflow is finalized.
* Railway deployment configuration is prepared.
* Final screenshots are captured for presentation.

### Tasks

* Streamlit UI App & Railway CI/CD.
* Refine dashboard layout based on feedback.
* Improve chart labels and table formatting.
* Add final Low, Medium, and High risk explanation.
* Prepare deployment configuration.
* Add Railway start command.
* Update README documentation.
* Capture final dashboard screenshots.

### Sprint 4 MVP Output

Refined dashboard MVP with deployment plan using GitHub Actions and Railway.

---

## Summary of User Stories

| User Story                                      | Main User               | Main Value                                                                   |
| ----------------------------------------------- | ----------------------- | ---------------------------------------------------------------------------- |
| User Story 1: EV Charging Demand Identification | Charging Point Operator | Identify locations with high EV demand and limited charging station coverage |
| User Story 2: Utility Grid Load Simulation      | Grid Operator           | Estimate charging load and detect possible grid stress areas                 |
| User Story 3: Dashboard and Deployment          | Local Council Planner   | View EV demand and grid load insights in a simple dashboard prototype        |

---

## Agile MVP Evolution

| Sprint   | MVP Stage                                    | Improvement                                             |
| -------- | -------------------------------------------- | ------------------------------------------------------- |
| Sprint 1 | Cleaned dataset and project setup            | Prepared the basic project foundation                   |
| Sprint 2 | EV demand and infrastructure gap analysis    | Added analytical value through EV-to-charger ratio      |
| Sprint 3 | Grid load simulation and dashboard prototype | Added load-risk simulation and visual interface         |
| Sprint 4 | Refined dashboard and deployment plan        | Improved usability and prepared Railway deployment plan |
