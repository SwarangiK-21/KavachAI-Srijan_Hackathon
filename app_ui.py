import flet as ft
import sqlite3
import joblib
import pandas as pd
from datetime import datetime

FEATURES   = ['call_hour', 'duration_sec', 'call_frequency', 'call_origin']
MODEL_PATH = 'kavach_model.pkl'
DB_PATH    = 'kavach_local.db'


def get_anomaly_reasons(call_hour, duration, frequency, origin, profile):
    contact_name, avg_duration, common_hour, avg_frequency, known_origin = profile
    reasons = []
    if abs(call_hour - common_hour) > 4:
        reasons.append(f"Unusual time — {contact_name} typically calls around {common_hour}:00")
    if duration > avg_duration * 2.5:
        reasons.append(f"Duration ({duration}s) far exceeds {contact_name}'s average ({int(avg_duration)}s)")
    if frequency < avg_frequency * 0.3:
        reasons.append(f"Low call frequency ({frequency}/wk) vs expected ({int(avg_frequency)}/wk)")
    if origin != known_origin:
        reasons.append(f"Origin mismatch — call from unknown/foreign network")
    return reasons


def check_call(phone_number, duration, frequency, origin):
    current_hour = datetime.now().hour
    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        return "error", None, [], "Model not found. Run engine.py first."

    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT contact_name, avg_duration, common_hour, avg_frequency, known_origin "
        "FROM trusted_contacts WHERE phone_number=?",
        (phone_number,)
    )
    profile = cursor.fetchone()
    conn.close()

    if not profile:
        return "unknown", None, ["No trust profile found for this number"], ""

    contact_name = profile[0]
    input_data   = pd.DataFrame([[current_hour, duration, frequency, origin]], columns=FEATURES)
    prediction   = model.predict(input_data)[0]
    score        = model.decision_function(input_data)[0]
    reasons      = get_anomaly_reasons(current_hour, duration, frequency, origin, profile)

    if prediction == -1:
        return "suspicious", contact_name, reasons, f"Anomaly score: {score:.3f}"
    else:
        return "trusted", contact_name, [], f"Confidence score: {score:.3f}"


# --- Simulation scenarios ---
SCENARIOS = [
    {
        "label":       "Normal call — Mom, 6 PM",
        "phone":       "9876543210",
        "duration":    110,
        "frequency":   7,
        "origin":      0,
    },
    {
        "label":       "Suspicious — Mom, 2 AM, unknown network",
        "phone":       "9876543210",
        "duration":    1500,
        "frequency":   1,
        "origin":      1,
    },
    {
        "label":       "Unknown number",
        "phone":       "0000000000",
        "duration":    60,
        "frequency":   1,
        "origin":      1,
    },
]


def main(page: ft.Page):
    page.title              = "KavachAI"
    page.window.width       = 420
    page.window.height      = 680
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment   = ft.MainAxisAlignment.CENTER
    page.bgcolor            = "#0D1117"
    page.padding            = 24

    # --- UI Elements ---
    shield_icon = ft.Icon(ft.Icons.SHIELD, color="#00C853", size=90)

    status_text = ft.Text(
        "System Protected",
        color="#00C853",
        size=20,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    contact_text = ft.Text("", color="#AAAAAA", size=13, text_align=ft.TextAlign.CENTER)

    score_text = ft.Text("", color="#555555", size=12, text_align=ft.TextAlign.CENTER)

    reasons_column = ft.Column(
        controls=[],
        spacing=6,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    detail_text = ft.Text(
        "Tap a simulation below to test KavachAI",
        color="#555555",
        size=13,
        text_align=ft.TextAlign.CENTER,
    )

    scenario_dropdown = ft.Dropdown(
        label="Select simulation",
        options=[ft.dropdown.Option(s["label"]) for s in SCENARIOS],
        value=SCENARIOS[0]["label"],
        bgcolor="#1C2128",
        color="#CCCCCC",
        border_color="#333333",
        focused_border_color="#1565C0",
        width=360,
    )

    def build_reason_chip(text, color):
        return ft.Container(
            content=ft.Text(text, color=color, size=12),
            bgcolor=color + "22",
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=10, vertical=6),
        )

    def set_state(verdict, contact, reasons, score_info):
        reasons_column.controls.clear()

        if verdict == "trusted":
            shield_icon.name  = ft.Icons.VERIFIED_USER
            shield_icon.color = "#00C853"
            status_text.value = "✅  VERIFIED: Trusted Behavior"
            status_text.color = "#00C853"
            contact_text.value = f"Caller: {contact}"
            detail_text.value  = "Call pattern matches known baseline."
            detail_text.color  = "#CCFF90"

        elif verdict == "suspicious":
            shield_icon.name  = ft.Icons.GPP_BAD
            shield_icon.color = "#FF1744"
            status_text.value = "⚠️  ALERT: Suspicious Call Detected"
            status_text.color = "#FF1744"
            contact_text.value = f"Caller claimed: {contact}"
            detail_text.value  = "Do NOT share sensitive info. Hang up and call back directly."
            detail_text.color  = "#FF8A80"
            for r in reasons:
                reasons_column.controls.append(build_reason_chip(r, "#FF5252"))

        elif verdict == "unknown":
            shield_icon.name  = ft.Icons.HELP_OUTLINE
            shield_icon.color = "#FF6D00"
            status_text.value = "Unknown Number"
            status_text.color = "#FF6D00"
            contact_text.value = "No trust profile found"
            detail_text.value  = "Proceed with caution — contact not recognised."
            detail_text.color  = "#FFD180"
            reasons_column.controls.append(build_reason_chip("Number not in trusted contacts", "#FF8C00"))

        elif verdict == "error":
            shield_icon.name  = ft.Icons.ERROR_OUTLINE
            shield_icon.color = "#888888"
            status_text.value = "System Error"
            status_text.color = "#888888"
            contact_text.value = ""
            detail_text.value  = score_info
            detail_text.color  = "#888888"

        score_text.value = score_info if verdict in ("trusted", "suspicious") else ""
        page.update()

    def on_simulate(e):
        selected_label = scenario_dropdown.value
        scenario = next((s for s in SCENARIOS if s["label"] == selected_label), SCENARIOS[0])
        verdict, contact, reasons, score_info = check_call(
            scenario["phone"],
            scenario["duration"],
            scenario["frequency"],
            scenario["origin"],
        )
        set_state(verdict, contact, reasons, score_info)

    def on_reset(e):
        shield_icon.name  = ft.Icons.SHIELD
        shield_icon.color = "#00C853"
        status_text.value = "System Protected"
        status_text.color = "#00C853"
        contact_text.value = ""
        score_text.value   = ""
        detail_text.value  = "Tap a simulation below to test KavachAI"
        detail_text.color  = "#555555"
        reasons_column.controls.clear()
        page.update()

    page.add(
        ft.Column(
            controls=[
                ft.Text("KavachAI", size=30, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                ft.Text("Voice Trust Shield", size=12, color="#444444"),
                ft.Container(height=10),
                shield_icon,
                ft.Container(height=12),
                status_text,
                contact_text,
                score_text,
                ft.Container(height=6),
                detail_text,
                ft.Container(height=8),
                reasons_column,
                ft.Container(height=20),
                scenario_dropdown,
                ft.Container(height=10),
                ft.FilledButton(
                    "Simulate Incoming Call",
                    on_click=on_simulate,
                    style=ft.ButtonStyle(
                        bgcolor="#1565C0",
                        color="#FFFFFF",
                    ),
                    width=240,
                ),
                ft.TextButton(
                    "Reset",
                    on_click=on_reset,
                    style=ft.ButtonStyle(color="#555555"),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=4,
        )
    )
    page.update()


if __name__ == "__main__":
    ft.app(target=main)