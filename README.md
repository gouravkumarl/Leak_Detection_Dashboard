# 💧 Leak Detection Dashboard

> **Real-time water anomaly detection & intelligent building analytics**

[![GitHub](https://img.shields.io/badge/GitHub-gouravkumarl-blue?logo=github&style=flat-square)](https://github.com/gouravkumarl/Leak_Detection_Dashboard)
[![Python](https://img.shields.io/badge/Python-3.9+-green?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io/)

---

## 🎯 Overview

A cutting-edge water analytics platform that **simulates building-level consumption patterns** and detects critical water system anomalies in real-time. Using advanced ML-driven heuristics and statistical analysis, it identifies:

| 🚨 Anomaly Type    | 📊 Detection Method                             |
| ------------------ | ----------------------------------------------- |
| **Leak**           | Sustained baseline elevation during night hours |
| **Burst**          | Extreme consumption spikes (>98.5th percentile) |
| **ScheduleChange** | Long-term consumption pattern shifts            |

---

## ✨ Key Features

🎨 **Interactive Streamlit Dashboard**

- Multi-building real-time simulation & monitoring
- Visual anomaly detection with consumption graphs
- Live anomaly score tracking

📈 **Advanced Analytics Pipeline**

- Synthetic event generation from historical patterns
- Temporal time-series modeling with minute-level granularity
- Rule-based anomaly detection with confidence scoring
- Comprehensive metrics: Confusion matrix, Accuracy, Per-class Recall

🔧 **Flexible Execution**

- Web-based dashboard mode
- CLI backend pipeline
- Configurable sensitivity thresholds

---

## 🏗️ Project Architecture

```
water-analytics-minopr/
├── 📊 app.py              → Streamlit UI & interactive simulation
├── ⚙️ core.py             → ML pipeline & analytics engine
├── 🖥️ main.py             → CLI backend executor
├── 📁 outputs/            → Generated metrics & artifacts
└── 📋 README.md           → This file
```

### Core Components

| File                   | Purpose                                          |
| ---------------------- | ------------------------------------------------ |
| **[app.py](app.py)**   | Streamlit dashboard with real-time visualization |
| **[core.py](core.py)** | Data pipeline, ML models, anomaly detection      |
| **[main.py](main.py)** | Headless pipeline execution                      |

---

## 🚀 Quick Start

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

## ⚙️ Configuration

### Control Panel Parameters

| Parameter                 | Range      | Default | Effect                   |
| ------------------------- | ---------- | ------- | ------------------------ |
| **Seed**                  | Any        | 42      | Reproducibility          |
| **Detection Sensitivity** | 1.0 - 10.0 | 3.5     | Anomaly threshold tuning |
| **Number of Buildings**   | 1 - 10     | 5       | Simulation scale         |
| **Duration (days)**       | 3 - 14     | 7       | Time window              |

---

## 📊 Data Pipeline

```
Raw Data (CSV)
    ↓
Event Detection (threshold-based)
    ↓
Pattern Modeling (hourly distribution)
    ↓
Synthetic Generation (per-building)
    ↓
Time-series Aggregation (15-min buckets)
    ↓
Anomaly Injection (leak, burst, schedule changes)
    ↓
Detection & Scoring
    ↓
Metrics Evaluation (confusion matrix, recall)
```

### Data Sources

- **Primary**: CSV files under `WEUSEDTO/` directory
- **Fallback**: Auto-generated synthetic Gamma-distributed flow data

---

## 📈 Model Performance

The system generates performance metrics including:

✅ **Accuracy** - Overall prediction correctness  
✅ **Confusion Matrix** - Per-class breakdown  
✅ **Recall** - Detection rate per anomaly type

---

## 🎮 Dashboard Features

### Real-Time Metrics

- **Model Accuracy** - Current model performance
- **Active Buildings** - Number of monitored sites
- **Data Points** - Total samples processed

### Interactive Views

- 🔍 Per-building consumption trends
- 📍 Anomaly alert highlighting
- 📉 Anomaly score visualization
- 🎯 Detailed performance reports

---

## 🔐 Repository & Deployment

```bash
# Check remote
git remote -v

# Push updates
git push origin master
```

**Live Repository**: [gouravkumarl/Leak_Detection_Dashboard](https://github.com/gouravkumarl/Leak_Detection_Dashboard)

---

## 📝 Notes

- Virtual environment (`venv/`) and cache (`__pycache__/`) are excluded via `.gitignore`
- Output artifacts saved to `outputs/run/`
- All timestamps in UTC ISO 8601 format
- Fully reproducible with seed control

---

## 💡 Tech Stack

| Technology     | Purpose                          |
| -------------- | -------------------------------- |
| **Streamlit**  | Interactive web dashboard        |
| **Pandas**     | Data manipulation & aggregation  |
| **NumPy**      | Numerical computing & statistics |
| **Matplotlib** | Time-series visualization        |

---

## 📧 Contact & Support

For issues, feature requests, or improvements, visit the [GitHub repository](https://github.com/gouravkumarl/Leak_Detection_Dashboard).

---

<div align="center">

**Built with ❤️ for water system intelligence**

![Last Updated](https://img.shields.io/badge/Last%20Updated-April%202026-blue?style=flat-square)

</div>
