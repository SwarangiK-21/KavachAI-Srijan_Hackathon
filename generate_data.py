import pandas as pd
import random

def generate_kavach_data(n_samples=1000):
    data = []

    # --- Normal call samples ---
    for _ in range(n_samples):
        call_hour      = random.randint(8, 22)        # Calls during the day
        duration_sec   = random.randint(30, 300)       # Short to medium duration
        call_frequency = random.randint(1, 10)         # Regular contact frequency
        call_origin    = random.choice([0, 0, 0, 1])  # Mostly known origin (0), rare unknown (1)
        label          = 0                             # Legitimate
        data.append([call_hour, duration_sec, call_frequency, call_origin, label])

    # --- Anomalous / spoofed samples ---
    for _ in range(150):
        call_hour      = random.randint(0, 5)          # Late-night calls (suspicious)
        duration_sec   = random.randint(600, 1800)     # Very long duration (suspicious)
        call_frequency = random.randint(0, 2)          # Rarely calls (suspicious)
        call_origin    = random.choice([1, 1, 1, 0])  # Mostly unknown/foreign origin (1)
        label          = 1                             # Spoofed / anomalous
        data.append([call_hour, duration_sec, call_frequency, call_origin, label])

    df = pd.DataFrame(data, columns=[
        'call_hour', 'duration_sec', 'call_frequency', 'call_origin', 'label'
    ])
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle rows
    df.to_csv('call_logs.csv', index=False)
    print(f"✅ Synthetic dataset 'call_logs.csv' created! ({len(df)} samples, 4 features)")
    print(df.head())

if __name__ == "__main__":
    generate_kavach_data()