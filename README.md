# Leak Detection Dashboard

> **Real-time water anomaly detection & intelligent building analytics**

[![GitHub](https://img.shields.io/badge/GitHub-gouravkumarl-blue?logo=github&style=flat-square)](https://github.com/gouravkumarl/Leak_Detection_Dashboard)
[![Python](https://img.shields.io/badge/Python-3.9+-green?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io/)

---

## Overview

A cutting-edge water analytics platform that **simulates building-level consumption patterns** and detects critical water system anomalies in real-time. Using advanced ML-driven heuristics and statistical analysis, it identifies three key anomaly types:

| Anomaly Type       | Detection Method                          |
| ------------------ | ----------------------------------------- |
| **Leak**           | Sustained baseline elevation during night |
| **Burst**          | Extreme consumption spikes (>98.5th %ile) |
| **ScheduleChange** | Long-term consumption pattern shifts      |

---

## Key Features

**Interactive Streamlit Dashboard**

- Multi-building real-time simulation & monitoring
- Visual anomaly detection with consumption graphs
- Live anomaly score tracking

**Advanced Analytics Pipeline**

- Synthetic event generation from historical patterns
- Temporal time-series modeling with minute-level granularity
- Rule-based anomaly detection with confidence scoring
- Comprehensive metrics: Confusion matrix, Accuracy, Per-class Recall

**Flexible Execution**

- Web-based dashboard mode
- CLI backend pipeline
- Configurable sensitivity thresholds

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EXECUTION MODES                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  app.py (Streamlit Web UI)    main.py (CLI Backend)        │
│         │                              │                    │
│         └──────────────┬───────────────┘                   │
│                        │                                    │
│                   core.py (Analytics)                       │
│                        │                                    │
│    ┌───────────────────┼────────────────────┐              │
│    │                   │                    │              │
│   Data              Events              Detection          │
│  Loading          Processing          & Metrics            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Project Files**

```
water-analytics-minopr/
├── app.py          → Streamlit UI & interactive simulation
├── core.py         → ML pipeline & analytics engine
├── main.py         → CLI backend executor
├── outputs/        → Generated metrics & artifacts
└── README.md       → This documentation
```

**Core Components**

| File    | Purpose                                  |
| ------- | ---------------------------------------- |
| app.py  | Streamlit dashboard with visualization   |
| core.py | Data pipeline, models, anomaly detection |
| main.py | Headless pipeline execution              |

---

## Quick Start

### Prerequisites

**Python 3.9+** with pip

### Installation

```bash
# Clone the repository
git clone https://github.com/gouravkumarl/Leak_Detection_Dashboard.git
cd water-analytics-minopr

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install streamlit pandas numpy matplotlib
```

### Run the Dashboard

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

### Run Backend Analysis

```bash
python main.py
```

---

## Configuration

### Control Panel Parameters

| Parameter             | Range      | Default | Effect                   |
| --------------------- | ---------- | ------- | ------------------------ |
| Seed                  | Any        | 42      | Reproducibility          |
| Detection Sensitivity | 1.0 - 10.0 | 3.5     | Anomaly threshold tuning |
| Number of Buildings   | 1 - 10     | 5       | Simulation scale         |
| Duration (days)       | 3 - 14     | 7       | Time window              |

---

## Data Processing Pipeline

```
┌──────────────────────────────────────────────────────────────┐
│                    INPUT SOURCES                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│     CSV Files (WEUSEDTO/)          Auto-generated           │
│            │                         Synthetic Data          │
│            └──────────────┬───────────────┘                 │
│                           │                                  │
│                    LOAD DATA MODULE                          │
│                           │                                  │
├──────────────────────────────────────────────────────────────┤
│  EVENT DETECTION    PATTERN MODELING    SYNTHETIC GEN        │
│  (Threshold)    →   (Hourly Dist)   →  (Per-building)      │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                  TIME-SERIES AGGREGATION                    │
│              (15-minute bucket resampling)                   │
│                           │                                  │
│                   ANOMALY INJECTION                          │
│  ┌──────────────┬────────────────┬──────────────┐           │
│  │              │                │              │            │
│  ▼              ▼                ▼              ▼            │
│ Leak       ScheduleChange      Burst       Baseline         │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                 DETECTION & SCORING                          │
│  Rule-based classification with anomaly scores              │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│            METRICS & PERFORMANCE EVALUATION                  │
│  Confusion Matrix | Accuracy | Per-class Recall             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Data Sources

- **Primary**: CSV files under `WEUSEDTO/` directory
- **Fallback**: Auto-generated synthetic Gamma-distributed flow data

---

## Anomaly Detection Logic

```
Input: Consumption Timeseries
         │
         ├─────────────────────────────────────┐
         │                                     │
    [Step 1]                             [Step 2]
  Calculate Baseline              Detect Anomaly Type
  (per 15-min slot)                       │
         │                                 │
         ├──────────────┬──────────────┬───┴────┐
         │              │              │        │
         ▼              ▼              ▼        ▼
    Residual        Schedule       Leak     Burst
    (actual - baseline)   Change   (night)  (extreme)
         │              │           │        │
         │         [Day 3+]      [01-04h]  [>98.5%ile]
         │         [↑ 1.05x]     [score>0.3]
         │              │           │        │
         └──────────────┴───────────┴────────┘
                        │
                    [PREDICTION]
                    (Normal/Leak/Burst/
                     ScheduleChange)
```

---

## Model Performance Metrics

---

## Dashboard Features

**Real-Time Metrics**

- Model Accuracy - Current model performance
- Active Buildings - Number of monitored sites
- Data Points - Total samples processed

**Interactive Views**

- Per-building consumption trends
- Anomaly alert highlighting
- Anomaly score visualization
- Detailed performance reports

---

## Execution Workflow

```
┌─────────────────────────┐
│   Select Execution      │
│       Mode              │
└────────────┬────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
[Web Dashboard]   [CLI Backend]
 (app.py)          (main.py)
    │                 │
    ├────────┬────────┤
    │        │        │
    ▼        ▼        ▼
 Set Seed  Load Data  Build Model
    │        │        │
    └────────┼────────┘
             │
      ┌──────┴──────────────┐
      │                     │
  For each Building    Simulate Events
      │                (per day)
      ▼                     │
 Generate Events ◄──────────┘
      │
      ▼
 Build Timeseries
      │
      ▼
 Inject Anomalies
      │
      ▼
 Detect Anomalies
      │
      ▼
 Calculate Metrics
      │
    ┌─┴──────────────┐
    │                │
    ▼                ▼
 Display UI     Print Results
```

---

## Repository & Deployment

**Live Repository**: [gouravkumarl/Leak_Detection_Dashboard](https://github.com/gouravkumarl/Leak_Detection_Dashboard)

```bash
# Check remote
git remote -v

# Push updates
git push origin master
```

---

## Tech Stack

| Technology | Purpose                         |
| ---------- | ------------------------------- |
| Streamlit  | Interactive web dashboard       |
| Pandas     | Data manipulation & aggregation |
| NumPy      | Numerical computing & stats     |
| Matplotlib | Time-series visualization       |

---

## Configuration Notes

- Virtual environment (`venv/`) and cache (`__pycache__/`) excluded via `.gitignore`
- Output artifacts saved to `outputs/run/`
- All timestamps in UTC ISO 8601 format
- Fully reproducible with seed control

---

## Support

For issues, feature requests, or improvements, visit the [GitHub repository](https://github.com/gouravkumarl/Leak_Detection_Dashboard).

---

<div align="center">

Built for water system intelligence

![Last Updated](https://img.shields.io/badge/Last%20Updated-April%202026-blue?style=flat-square)

</div>
