# KavachAI: Voice Trust & Anomaly Detection System 🛡️

**KavachAI** is an on-device security layer designed to combat the rising threat of AI-driven voice spoofing and telephony fraud. By leveraging local Machine Learning and behavioral analytics, KavachAI validates the authenticity of incoming calls without ever compromising user privacy.

---

## 🚀 Problem Statement
Traditional caller ID systems rely on phone numbers, which are easily spoofed. With the advent of generative AI, scammers can now mimic voices with terrifying accuracy. **KavachAI** solves this by moving from "Identity-based trust" to **"Behavior-based trust."**

### Core Constraints Met:
- **100% On-Device:** No call metadata or audio leaves the device.
- **Zero Latency:** Real-time inference performed locally via an optimized engine.
- **Privacy-First:** Utilizes a local SQLite vault for personal baseline storage.

---

## 🛠️ Technical Architecture

KavachAI is built on a decoupled architecture to ensure modularity and high performance:

1. **Data Layer (`generate_data.py`):** Generates synthetic call logs to simulate human behavioral patterns (Time, Duration, Frequency).
2. **Storage Layer (`init_db.py`):** A secure **Local SQLite Database** that stores the "Golden Baseline" for trusted contacts.
3. **Inference Engine (`engine.py`):** A Machine Learning pipeline using **Isolation Forest (Anomaly Detection)** to identify suspicious deviations from the baseline.
4. **Application Logic (`main.py`):** The core integration script that performs the real-time lookup and trust-scoring.
5. **Presentation Layer (`app_ui.py`):** A reactive dashboard built with **Flet** providing instant visual feedback (Verified vs. Alert).

---

## 🧠 Machine Learning Workflow
KavachAI doesn't use a "blocklist." It uses an **Isolation Forest** model to detect anomalies.
- **Normal Behavior:** Calls that occur within the expected hour and duration window stored in the local SQLite profile.
- **Anomalous Behavior:** Out-of-window calls (e.g., 3:00 AM) or duration spikes (e.g., 40 mins for a 2-min contact) trigger an immediate **Trust Score reduction**.
