import sqlite3
import joblib
import pandas as pd
from datetime import datetime

# 1. Load the trained AI Model
model = joblib.load('kavach_model.pkl')

def check_incoming_call(phone_number, duration):
    # Get current time for the feature
    current_hour = datetime.now().hour
    
    # 2. SQL Lookup: Get the "Trust Profile" from SQLite
    conn = sqlite3.connect('kavach_local.db')
    cursor = conn.cursor()
    cursor.execute("SELECT avg_duration, common_hour FROM trusted_contacts WHERE phone_number=?", (phone_number,))
    profile = cursor.fetchone()
    conn.close()

    if profile:
        print(f"\nChecking Call from Known Contact: {phone_number}")
        
        # 3. AI Inference: Check for anomalies
        # We pass the current call data into the model
        input_data = pd.DataFrame([[current_hour, duration]], columns=['call_hour', 'duration_sec'])
        prediction = model.predict(input_data)
        
        # Isolation Forest returns -1 for anomalies and 1 for normal
        if prediction[0] == -1:
            print("⚠️ KAVACHAI ALERT: SUSPICIOUS ACTIVITY DETECTED!")
            print(f"Reason: Call pattern (Hour: {current_hour}, Duration: {duration}s) deviates from local baseline.")
        else:
            print("✅ KAVACHAI VERIFIED: Call matches trusted behavior.")
    else:
        print(f"\nNew/Unknown Number: {phone_number}. Proceed with caution.")

# --- SIMULATION ---
# Scenario A: Normal call (e.g., calling at 6 PM for 2 mins)
check_incoming_call('9876543210', 120)

# Scenario B: Suspicious call (e.g., calling at 3 AM for 20 mins)
# Note: This will trigger an alert if the model was trained with the 'generate_data' logic
check_incoming_call('9876543210', 1800)