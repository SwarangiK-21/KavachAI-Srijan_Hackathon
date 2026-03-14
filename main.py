import sqlite3
import joblib
import pandas as pd
from datetime import datetime

FEATURES = ['call_hour', 'duration_sec', 'call_frequency', 'call_origin']
MODEL_PATH = 'kavach_model.pkl'
DB_PATH    = 'kavach_local.db'

def get_anomaly_reasons(call_hour, duration, frequency, origin, profile):
    """
    Build a human-readable explanation of WHY a call is suspicious.
    Compares incoming call data against the trusted contact's baseline profile.
    """
    contact_name, avg_duration, common_hour, avg_frequency, known_origin = profile
    reasons = []

    hour_diff = abs(call_hour - common_hour)
    if hour_diff > 4:
        reasons.append(
            f"call time ({call_hour}:00) is unusual — {contact_name} usually calls around {common_hour}:00"
        )

    if duration > avg_duration * 2.5:
        reasons.append(
            f"call duration ({duration}s) is much longer than {contact_name}'s average ({int(avg_duration)}s)"
        )

    if frequency < avg_frequency * 0.3:
        reasons.append(
            f"call frequency ({frequency}/week) is much lower than expected ({int(avg_frequency)}/week)"
        )

    if origin != known_origin:
        reasons.append(
            f"call origin (unknown/foreign network) differs from {contact_name}'s known network"
        )

    return reasons


def check_incoming_call(phone_number, duration, frequency=5, origin=0):
    """
    Main KavachAI verification function.
    Returns: dict with verdict, score, contact name, and reasons.
    """
    current_hour = datetime.now().hour

    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        print("❌ Model not found. Run engine.py first.")
        return None

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT contact_name, avg_duration, common_hour, avg_frequency, known_origin "
        "FROM trusted_contacts WHERE phone_number=?",
        (phone_number,)
    )
    profile = cursor.fetchone()
    conn.close()

    print(f"\n{'='*55}")
    print(f"  KavachAI — Incoming Call from {phone_number}")
    print(f"{'='*55}")

    if not profile:
        print("⚠️  UNKNOWN NUMBER — No trust profile found.")
        print("   This number is not in your trusted contacts.")
        print("   Recommendation: Proceed with caution.\n")
        return {"verdict": "unknown", "reasons": ["No trust profile found"]}

    contact_name = profile[0]
    print(f"  Contact : {contact_name}")
    print(f"  Time    : {current_hour}:00 | Duration: {duration}s | Freq: {frequency}/week | Origin: {'Known' if origin == 0 else 'Unknown'}")

    # Build input for model using deviation from baseline
    input_data = pd.DataFrame(
        [[current_hour, duration, frequency, origin]],
        columns=FEATURES
    )
    prediction    = model.predict(input_data)[0]
    anomaly_score = model.decision_function(input_data)[0]

    reasons = get_anomaly_reasons(current_hour, duration, frequency, origin, profile)

    if prediction == -1:
        print(f"\n  ⚠️  KAVACHAI ALERT: SUSPICIOUS ACTIVITY DETECTED!")
        print(f"  Anomaly score : {anomaly_score:.4f} (negative = more suspicious)")
        if reasons:
            print(f"  Reasons detected:")
            for r in reasons:
                print(f"    • {r.capitalize()}")
        print(f"\n  Recommendation: Do NOT share sensitive info. Hang up and call {contact_name} back directly.\n")
        return {"verdict": "suspicious", "score": anomaly_score, "contact": contact_name, "reasons": reasons}
    else:
        print(f"\n  ✅  KAVACHAI VERIFIED: Call matches trusted behavior.")
        print(f"  Confidence score : {anomaly_score:.4f}")
        print(f"  Recommendation   : Safe to proceed.\n")
        return {"verdict": "trusted", "score": anomaly_score, "contact": contact_name, "reasons": []}


if __name__ == "__main__":
    print("\n" + "="*55)
    print("  KavachAI — SIMULATION MODE")
    print("="*55)

    # Scenario A: Normal call from Mom (evening, short, frequent, known network)
    print("\n[Scenario A] Normal call from Mom at 6 PM")
    check_incoming_call('9876543210', duration=110, frequency=7, origin=0)

    # Scenario B: Suspicious call — midnight, very long, low freq, unknown origin
    print("[Scenario B] Suspicious call from 'Mom' at 2 AM, 20 min, unknown network")
    check_incoming_call('9876543210', duration=1500, frequency=1, origin=1)

    # Scenario C: Unknown number
    print("[Scenario C] Unknown number")
    check_incoming_call('0000000000', duration=60, frequency=1, origin=1)