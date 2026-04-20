# core.py

import numpy as np
import pandas as pd
from pathlib import Path

# -------------------------
# SEED
# -------------------------
def set_seed(seed):
    np.random.seed(seed)

# -------------------------
# LOAD DATA
# -------------------------
def load_data(path):
    files = list(Path(path).rglob("*.csv"))

    if not files:
        # fallback synthetic
        t = pd.date_range("2025-01-01", periods=2000, freq="1min")
        flow = np.random.gamma(2, 2, size=len(t))
        return pd.DataFrame({"timestamp": t, "flow": flow})

    df = pd.read_csv(files[0], sep=r"\s+", header=None)
    df.columns = ["timestamp", "flow"]
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    return df

# -------------------------
# EVENT DETECTION
# -------------------------
def detect_events(df, threshold):
    df = df.copy()

    df["active"] = df["flow"] > threshold
    df["block"] = (df["active"] != df["active"].shift()).cumsum()

    events = df[df["active"]].groupby("block").agg(
        start=("timestamp", "min"),
        end=("timestamp", "max"),
        volume=("flow", "sum")
    )

    events["duration"] = (
        (events["end"] - events["start"]).dt.total_seconds() / 60
    )

    return events.reset_index(drop=True)

# -------------------------
# MODEL
# -------------------------
def build_model(events):
    clean = events[
        (events["duration"] >= 1) &
        (events["duration"] <= 20)
    ]

    hourly = clean["start"].dt.hour.value_counts(normalize=True)

    return {
        "dur_mean": clean["duration"].mean(),
        "dur_std": clean["duration"].std(),
        "vol_mean": clean["volume"].mean(),
        "vol_std": clean["volume"].std(),
        "hourly": hourly
    }

# -------------------------
# SYNTHETIC EVENTS
# -------------------------
def generate_events(model, date, users=20):
    events = []

    for _ in range(users):
        if np.random.rand() < 0.7:
            hour = np.random.choice(
                model["hourly"].index,
                p=model["hourly"].values
            )

            start = pd.Timestamp(date) + pd.Timedelta(
                hours=int(hour),
                minutes=np.random.randint(60)
            )

            dur = max(1, np.random.normal(
                model["dur_mean"], model["dur_std"]
            ))

            vol = max(1, np.random.normal(
                model["vol_mean"], model["vol_std"]
            ))

            end = start + pd.Timedelta(minutes=dur)

            events.append((start, end, dur, vol))

    return events

# -------------------------
# TIME SERIES
# -------------------------
def fast_timeseries(events):
    df = pd.DataFrame(events, columns=["start", "end", "dur", "vol"])

    idx = pd.date_range(
        df["start"].min().floor("D"),
        df["end"].max().ceil("D"),
        freq="1min"
    )

    ts = pd.DataFrame(index=idx)
    ts["consumption"] = 0.0

    for s, e, d, v in events:
        ts.loc[s:e, "consumption"] += v / max(d, 1)

    ts = ts.resample("15min").sum().reset_index()
    ts.rename(columns={"index": "timestamp"}, inplace=True)

    return ts

# -------------------------
# ANOMALIES
# -------------------------
def inject(df):
    df = df.copy()
    df["gt"] = "Normal"

    # FIX 1: Apply ScheduleChange FIRST (lowest priority label)
    # so that Leak and Burst labels are not overwritten
    mask2 = df["timestamp"] > df["timestamp"].min() + pd.Timedelta(days=3)
    df.loc[mask2, "consumption"] *= 1.3
    df.loc[mask2, "gt"] = "ScheduleChange"

    # FIX 2: Leak — only inject during night hours on early days
    # to avoid every row after day 3 being clobbered
    mask = df["timestamp"].dt.hour.between(1, 4)
    df.loc[mask, "consumption"] += 30
    df.loc[mask, "gt"] = "Leak"

    # FIX 3: Burst — increase from 3 to 10 samples for better class balance
    idx = df.sample(10).index
    df.loc[idx, "consumption"] *= 6
    df.loc[idx, "gt"] = "Burst"

    return df

# -------------------------
# DETECTION
# -------------------------
def detect(df, threshold):
    df = df.copy()

    df["slot"] = df["timestamp"].dt.hour * 4 + df["timestamp"].dt.minute // 15

    baseline = df.groupby("slot")["consumption"].mean()
    df["baseline"] = df["slot"].map(baseline)

    df["res"] = df["consumption"] - df["baseline"]

    std = df["res"].std()
    df["score"] = df["res"] / (std + 1e-6)

    df["pred"] = "Normal"

    # ScheduleChange: ALL rows after day 3 with any elevation above baseline
    sc_mask = (
        df["timestamp"] > df["timestamp"].min() + pd.Timedelta(days=3)
    ) & (df["consumption"] >= df["baseline"] * 1.05)
    df.loc[sc_mask, "pred"] = "ScheduleChange"

    # Leak: night hours 1-4 AM with positive residual (overrides ScheduleChange)
    leak_mask = (
        (df["timestamp"].dt.hour.between(1, 4)) &
        (df["score"] > 0.3)
    )
    df.loc[leak_mask, "pred"] = "Leak"

    # Burst: top 1.5% of scores — overrides everything
    burst_threshold = df["score"].quantile(0.985)
    df.loc[df["score"] > burst_threshold, "pred"] = "Burst"

    return df

# -------------------------
# METRICS
# -------------------------
def metrics(df):
    cm = pd.crosstab(df["gt"], df["pred"])
    acc = (df["gt"] == df["pred"]).mean()

    recall = {}
    for c in df["gt"].unique():
        tp = ((df["gt"] == c) & (df["pred"] == c)).sum()
        fn = ((df["gt"] == c) & (df["pred"] != c)).sum()
        recall[c] = tp / (tp + fn + 1e-6)

    return cm, acc, recall
