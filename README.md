# KavachAI: Voice Trust & Anomaly Detection System 🛡️

**KavachAI** is an on-device security layer designed to combat the rising threat of AI-driven voice spoofing and telephony fraud. By leveraging local Machine Learning and behavioral analytics, KavachAI validates the authenticity of incoming calls without ever compromising user privacy.

---

## 🚀 Problem Statement

Traditional caller ID systems rely on phone numbers, which are easily spoofed. With the advent of generative AI, scammers can now mimic voices with terrifying accuracy. **KavachAI** solves this by moving from "Identity-based trust" to **"Behavior-based trust."**

### Core Constraints Met

- **100% On-Device:** No call metadata or audio leaves the device.
- **Zero Latency:** Real-time inference performed locally via an optimized engine.
- **Privacy-First:** Utilizes a local SQLite vault for personal baseline storage.

---

## 🛠️ Technical Architecture

KavachAI is built on a decoupled architecture to ensure modularity and high performance:

| Layer | File | Responsibility |
|---|---|---|
| Data Layer | `generate_data.py` | Generates synthetic call logs to simulate human behavioral patterns (Time, Duration, Frequency) |
| Storage Layer | `init_db.py` | A secure Local SQLite Database that stores the "Golden Baseline" for trusted contacts |
| Inference Engine | `engine.py` | ML pipeline using Isolation Forest (Anomaly Detection) to identify suspicious deviations |
| Application Logic | `main.py` | Core integration script that performs real-time lookup and trust-scoring |
| Presentation Layer | `app_ui.py` | Reactive dashboard built with Flet providing instant visual feedback (Verified vs. Alert) |

---

## 🧠 Machine Learning Workflow

KavachAI doesn't use a "blocklist." It uses an **Isolation Forest** model to detect anomalies.

- **Normal Behavior:** Calls that occur within the expected hour and duration window stored in the local SQLite profile.
- **Anomalous Behavior:** Out-of-window calls (e.g., 3:00 AM) or duration spikes (e.g., 40 mins for a 2-min contact) trigger an immediate **Trust Score reduction**.
```
Incoming Call
     │
     ▼
SQLite Lookup ──► Contact Known? ──No──► ⚠️ Unknown Number
     │
    Yes
     │
     ▼
Isolation Forest
     │
     ├── Normal Pattern ──► ✅ VERIFIED
     └── Anomaly Detected ──► 🚨 ALERT
```

---

## ⚡ Setup & Installation

Ensure you have **Python 3.10+** installed before proceeding.

### 1. Clone the Repository
```bash
git clone https://github.com/SwarangiK-21/KavachAI_Srijan_Hackathon.git
cd KavachAI_Srijn_Hackathon
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the MVP

Run the scripts in this **specific order** to simulate the full data-to-UI pipeline.

### Step 1 — Generate Synthetic Data
Creates the historical dataset required for training.
```bash
python generate_data.py
```

### Step 2 — Initialize Secure Vault
Sets up the local SQLite database for trusted contact storage.
```bash
python init_db.py
```

### Step 3 — Train the AI Inference Engine
Trains the Isolation Forest model and saves it as `kavach_model.pkl`.
```bash
python engine.py
```

### Step 4 — Launch the KavachAI Dashboard
Opens the Flet-based UI to simulate and visualize call trust.
```bash
python app_ui.py
```

---

## 📁 Project Structure
```
KavachAI_Srijan_Hackathon/
│
├── generate_data.py      # Synthetic dataset generation
├── init_db.py            # SQLite vault initialization
├── engine.py             # Isolation Forest training
├── main.py               # Core logic & trust scoring
├── app_ui.py             # Flet dashboard UI
├── kavach_model.pkl      # Saved ML model (generated at runtime)
├── kavach_local.db       # Local SQLite database (generated at runtime)
├── call_logs.csv         # Synthetic call data (generated at runtime)
└── requirements.txt      # Python dependencies
```

---

## 🔒 Privacy Guarantee

> KavachAI is designed with a **privacy-first** philosophy. All data — call logs, behavioral baselines, and ML models — reside exclusively on the user's device. Nothing is transmitted to any external server.

---

*Built for Srijan Hackathon* 🏆
*Built by TEAM KB : Swarangi Kothawade & Suraj Madane* 🏆

