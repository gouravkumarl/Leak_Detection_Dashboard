# Leak Detection Dashboard

A lightweight water analytics project for simulating building-level consumption and detecting anomalies such as:
- **Leak**
- **Burst**
- **ScheduleChange**

It includes:
- A **Streamlit dashboard** ([app.py](app.py))
- A **core analytics pipeline** ([core.py](core.py))
- A **CLI backend runner** ([main.py](main.py))

## Features

- Synthetic event generation from learned event patterns
- Time-series generation and anomaly injection
- Rule-based anomaly detection with anomaly score
- Metrics output: confusion matrix, accuracy, recall
- Interactive dashboard for multi-building simulation

## Project Structure

- [app.py](app.py): Streamlit UI and end-to-end simulation runner
- [core.py](core.py): Data loading, event detection, modeling, simulation, anomaly detection, and metrics
- [main.py](main.py): Terminal-based pipeline execution
- [outputs/run/](outputs/run/): Sample output artifacts

## Requirements

Python 3.9+ recommended.

Install dependencies:

- `streamlit`
- `pandas`
- `numpy`
- `matplotlib`

## Quick Start

1. Create/activate a virtual environment.
2. Install required packages.
3. Run either dashboard or backend mode.

### Run Dashboard

Start the Streamlit app from project root:

`streamlit run app.py`

### Run Backend Pipeline

`python main.py`

## Data Source

The loader in [core.py](core.py) looks for CSV files under `WEUSEDTO/`.
If no CSV is found, it automatically generates fallback synthetic data.

## Notes

- `.gitignore` excludes local runtime artifacts and virtual environments.
- Current branch is pushed to GitHub repository:
  [gouravkumarl/Leak_Detection_Dashboard](https://github.com/gouravkumarl/Leak_Detection_Dashboard)
