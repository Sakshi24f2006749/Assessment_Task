# Customer Behavioral Conversion Analytics Dashboard

## Project Overview

This project implements an end-to-end analytics solution for tracking customer behavioral conversion patterns using a multi-session clickstream dataset.

The application performs:

- Automated ETL processing
- Data cleansing and standardization
- Feature engineering
- Relational database persistence
- REST API analytics
- Interactive dashboard visualization
- Asynchronous CSV export

---

## Tech Stack

### Backend
- Python
- Flask
- SQLite

### Data Engineering
- Pandas
- NumPy
- OpenPyXL

### Frontend
- HTML
- CSS
- Bootstrap 5
- Chart.js

---

## Architecture

### Phase 1 – Data Engineering

- Data Extraction
- Missing Value Handling
- Duplicate Removal
- Categorical Standardization
- Feature Engineering
  - Recency
  - Dwell Time
  - Engagement Score
  - Purchase Prediction
- SQLite Data Persistence

### Phase 2 – Analytics Dashboard

REST APIs:

- /api/pipeline-metrics
- /api/kpis
- /api/high-value-users
- /api/device-distribution
- /api/conversion-overview

Dashboard Components:

- Pipeline Metrics
- Behavioral KPIs
- Device Distribution Chart
- Conversion Overview Chart
- Paginated High Value Users Table

### Phase 3 – Asynchronous Processing

- Background CSV Export
- Non-blocking Execution
- Downloadable Analytics Reports

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd Assessment_Task
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run ETL Pipeline

```bash
python etl/run_pipeline.py
```

---

## Start Dashboard

```bash
python app.py
```

Open:

http://127.0.0.1:5000

---

## Features Implemented

✔ Data Cleaning

✔ Feature Engineering

✔ SQLite Database Design

✔ Flask REST APIs

✔ KPI Dashboard

✔ Device Analytics

✔ Conversion Analytics

✔ Pagination

✔ Async CSV Export

✔ ETL Monitoring

✔ Responsive Design

---

## Author

Sakshi Pathak
