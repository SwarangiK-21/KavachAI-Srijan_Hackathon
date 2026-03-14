# KavachAI: The Digital Shield Against Voice Spoofing 🛡️

**KavachAI** is an on-device security layer designed to combat the rising threat of AI-driven voice spoofing and telephony fraud. By leveraging local Machine Learning and multi-factor behavioral analytics, KavachAI validates the authenticity of incoming calls — without ever compromising user privacy.

---

## 🚀 Problem Statement

Traditional caller ID systems rely on phone numbers, which are easily spoofed. With the advent of generative AI, scammers can now mimic voices with terrifying accuracy. **KavachAI** solves this by moving from "Identity-based trust" to **"Behavior-based trust."**

### Core Constraints Met

- **100% On-Device:** No call metadata or audio ever leaves the device.
- **Zero Latency:** Real-time inference performed locally via an optimized ML engine.
- **Privacy-First:** A local SQLite vault stores personal behavioral baselines — no cloud, no PII exposure.
- **GDPR / DPDP Compliant:** Zero knowledge architecture ensures full regulatory compliance.

---

## 🛠️ Technical Architecture

KavachAI is built on a decoupled, modular architecture for high performance and maintainability:

| Layer | File | Responsibility |
|---|---|---|
| Data Layer | `generate_data.py` | Generates synthetic call logs simulating behavioral patterns across 4 features: Time, Duration, Frequency, and Origin |
| Storage Layer | `init_db.py` | Secure local SQLite vault storing the "Golden Baseline" for trusted contacts (name, avg duration, typical hour, frequency, known origin) |
| Inference Engine | `engine.py` | ML pipeline using Isolation Forest trained on 4 behavioral features to detect suspicious deviations |
| Application Logic | `main.py` | Core integration: performs real-time SQL lookup, multi-factor trust scoring, and generates explainable alert reasons |
| Presentation Layer | `app_ui.py` | Reactive Flet dashboard providing instant visual feedback (Verified ✅ / Alert ⚠️ / Unknown 🔶) with per-reason anomaly chips |

---

## 🧠 Machine Learning Workflow

KavachAI doesn't use a blocklist. It uses an **Isolation Forest** anomaly detection model trained on 4 behavioral features:

| Feature | Description | Normal Range | Suspicious Signal |
|---|---|---|---|
| `call_hour` | Hour the call is received | 8 AM – 10 PM | Midnight / early morning |
| `duration_sec` | Duration of the call in seconds | 30s – 300s | 600s+ (abnormally long) |
| `call_frequency` | How often this contact calls per week | 3 – 10 | 0 – 2 (rarely calls) |
| `call_origin` | Whether the call origin is known (0) or foreign/unknown (1) | 0 (known) | 1 (unknown/foreign) |

### Trust Scoring Flow

```
Incoming Call
     │
     ▼
SQLite Lookup ──► Contact Known? ──No──► 🔶 Unknown Number Alert
     │
    Yes
     │
     ▼
Multi-Factor Baseline Comparison
(call_hour vs common_hour, duration vs avg_duration,
 frequency vs avg_frequency, origin vs known_origin)
     │
     ▼
Isolation Forest ML Inference
     │
     ├── Normal Pattern ──► ✅ VERIFIED — Safe to proceed
     └── Anomaly Detected ──► ⚠️ ALERT — Explainable reasons shown
```

### Explainable Alerts (Human-in-the-Loop)

When an anomaly is detected, KavachAI doesn't just flag — it **explains**:
- *"Unusual time — Mom typically calls around 18:00"*
- *"Duration (1500s) far exceeds Mom's average (120s)"*
- *"Origin mismatch — call from unknown/foreign network"*
- *"Low call frequency (1/wk) vs expected (7/wk)"*

---

## ⚡ Setup & Installation

Ensure you have **Python 3.10+** installed before proceeding.

### 1. Clone the Repository
```bash
git clone https://github.com/SwarangiK-21/KavachAI_Srijan_Hackathon.git
cd KavachAI_Srijan_Hackathon
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the MVP

> ⚠️ **Important:** Always delete any existing `kavach_local.db` before re-running `init_db.py` to avoid schema conflicts.

Run the scripts in this **specific order** to simulate the full data-to-UI pipeline.

### Step 1 — Generate Synthetic Data
Creates a 1150-sample historical dataset with 4 behavioral features for training.
```bash
python generate_data.py
```

### Step 2 — Initialize Secure Vault
Sets up the local SQLite database with trusted contact baseline profiles.
```bash
python init_db.py
```

### Step 3 — Train the AI Inference Engine
Trains the Isolation Forest on normal call patterns and saves it as `kavach_model.pkl`.
```bash
python engine.py
```

### Step 4 — (Optional) Run CLI Test
Validates all 3 scenarios — normal call, suspicious call, and unknown number — directly in the terminal.
```bash
python main.py
```

### Step 5 — Launch the KavachAI Dashboard
Opens the Flet-based UI to simulate and visualize call trust scoring with explainable alerts.
```bash
python app_ui.py
```

---

## 📁 Project Structure

```
KavachAI_Srijan_Hackathon/
│
├── generate_data.py      # Synthetic dataset generation (4 features, 1150 samples)
├── init_db.py            # SQLite vault initialization (6-column contact profiles)
├── engine.py             # Isolation Forest training with sanity checks
├── main.py               # Core logic, multi-factor trust scoring & explainable alerts
├── app_ui.py             # Flet dashboard UI with anomaly reason chips
├── kavach_model.pkl      # Saved ML model (generated at runtime)
├── kavach_local.db       # Local SQLite database (generated at runtime)
├── call_logs.csv         # Synthetic call data (generated at runtime)
└── requirements.txt      # Python dependencies
```

---

## 📦 Requirements

```
pandas
scikit-learn
joblib
flet
```

Generate `requirements.txt` with:
```bash
pip freeze > requirements.txt
```

---

## 🔒 Privacy Guarantee

> KavachAI is designed with a **privacy-first** philosophy. All data — call logs, behavioral baselines, and ML models — reside exclusively on the user's device. Nothing is transmitted to any external server. Zero PII leaves the handset.

---

## 🏆 Built for Srijan Hackathon — Problem Statement 9
*Detect Fake Calls from Well-Known Contacts*

*Built by **Team KB** — Swarangi Kothawade & Suraj Madane* 🏆
