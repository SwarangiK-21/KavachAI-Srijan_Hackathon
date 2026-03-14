import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

FEATURES = ['call_hour', 'duration_sec', 'call_frequency', 'call_origin']

def train_engine():
    df = pd.read_csv('call_logs.csv')

    # Validate all required features exist
    missing = [f for f in FEATURES if f not in df.columns]
    if missing:
        raise ValueError(f"Missing features in CSV: {missing}. Run generate_data.py first.")

    # Train only on normal (label=0) samples — IsolationForest learns what "normal" looks like
    normal_df = df[df['label'] == 0]
    print(f"Training on {len(normal_df)} normal samples with features: {FEATURES}")

    model = IsolationForest(
        n_estimators=200,
        contamination=0.10,   # ~10% anomaly rate expected
        random_state=42
    )
    model.fit(normal_df[FEATURES])

    joblib.dump(model, 'kavach_model.pkl')
    print("✅ AI Inference Engine trained and saved as 'kavach_model.pkl'!")

    # Quick sanity check
    test_normal    = pd.DataFrame([[14, 120, 7, 0]], columns=FEATURES)
    test_anomalous = pd.DataFrame([[2,  1500, 1, 1]], columns=FEATURES)
    pred_n = model.predict(test_normal)[0]
    pred_a = model.predict(test_anomalous)[0]
    print(f"Sanity check — Normal call prediction : {'✅ Normal' if pred_n == 1 else '⚠️ Flagged (adjust contamination)'}")
    print(f"Sanity check — Anomalous call prediction: {'✅ Flagged' if pred_a == -1 else '⚠️ Missed (adjust contamination)'}")

if __name__ == "__main__":
    train_engine()