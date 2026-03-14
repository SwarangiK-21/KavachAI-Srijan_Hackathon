import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# 1. Load data
df = pd.read_csv('call_logs.csv')

# 2. Train Anomaly Detector (Isolation Forest)
# We train only on 'normal' looking features
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(df[['call_hour', 'duration_sec']])

# 3. Save the model for the app to use
joblib.dump(model, 'kavach_model.pkl')
print("✅ AI Inference Engine trained and saved as 'kavach_model.pkl'!")

model.fit(df[['call_hour', 'duration_sec']]) # This is the "Study" part
joblib.dump(model, 'kavach_model.pkl')       # This is the "Save" part