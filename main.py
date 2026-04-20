# main.py

from core import *
import pandas as pd

def main():
    print("Running backend pipeline...")

    set_seed(42)

    df = load_data("WEUSEDTO")
    events = detect_events(df, 3.5)
    model = build_model(events)

    all_df = []

    for b in range(3):
        ev = []
        for d in pd.date_range("2025-01-01", periods=5):
            ev.extend(generate_events(model, d))

        ts = fast_timeseries(ev)
        ts = inject(ts)
        ts = detect(ts, 3.5)

        ts["building"] = f"B{b+1}"
        all_df.append(ts)

    campus = pd.concat(all_df)

    cm, acc, recall = metrics(campus)

    print("\nAccuracy:", acc)
    print("\nConfusion Matrix:\n", cm)
    print("\nRecall:\n", recall)

    print("\n✅ Backend run complete!")

if __name__ == "__main__":
    main()