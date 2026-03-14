import flet as ft
import sqlite3
import joblib
import pandas as pd
from datetime import datetime

def check_incoming_call(phone_number, duration):
    current_hour = datetime.now().hour
    try:
        model = joblib.load('kavach_model.pkl')
        conn = sqlite3.connect('kavach_local.db')
        cursor = conn.cursor()
        cursor.execute("SELECT avg_duration, common_hour FROM trusted_contacts WHERE phone_number=?", (phone_number,))
        profile = cursor.fetchone()
        conn.close()

        if profile:
            input_data = pd.DataFrame([[current_hour, duration]], columns=['call_hour', 'duration_sec'])
            prediction = model.predict(input_data)
            return prediction[0] == -1  # True = suspicious
        return None  # Unknown number
    except Exception as e:
        print(f"Error: {e}")
        return None

def main(page: ft.Page):
    page.title = "KavachAI Dashboard"
    page.window.width = 400
    page.window.height = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#121212"

    shield = ft.Icon(ft.Icons.SHIELD, color="#00C853", size=100)
    status_label = ft.Text("System Protected", color="#00C853", size=20, weight=ft.FontWeight.BOLD)
    detail_text = ft.Text("Awaiting call simulation...", color="#888888", size=14)

    def on_simulate(e):
        result_b = check_incoming_call('9876543210', 1800)

        if result_b is True:
            shield.name = ft.Icons.GPP_BAD
            shield.color = "#FF1744"
            status_label.value = "⚠️ ALERT: SUSPICIOUS CALL"
            status_label.color = "#FF1744"
            detail_text.value = "Anomalous pattern detected. Proceed with caution."
            detail_text.color = "#FF8A80"
        elif result_b is False:
            shield.name = ft.Icons.VERIFIED_USER
            shield.color = "#00C853"
            status_label.value = "✅ VERIFIED: Trusted Behavior"
            status_label.color = "#00C853"
            detail_text.value = "Call pattern matches known baseline."
            detail_text.color = "#CCFF90"
        else:
            shield.name = ft.Icons.HELP_OUTLINE
            shield.color = "#FF6D00"
            status_label.value = "Unknown Number"
            status_label.color = "#FF6D00"
            detail_text.value = "No trust profile found. Proceed carefully."
            detail_text.color = "#FFD180"

        page.update()

    def on_reset(e):
        shield.name = ft.Icons.SHIELD
        shield.color = "#00C853"
        status_label.value = "System Protected"
        status_label.color = "#00C853"
        detail_text.value = "Awaiting call simulation..."
        detail_text.color = "#888888"
        page.update()

    page.add(
        ft.Column(
            controls=[
                ft.Text("KavachAI", size=32, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                ft.Text("Voice Trust System", size=13, color="#555555"),
                ft.Container(height=30),
                shield,
                ft.Container(height=16),
                status_label,
                ft.Container(height=8),
                detail_text,
                ft.Container(height=40),
                ft.ElevatedButton(
                    "Simulate Incoming Call",
                    on_click=on_simulate,
                    bgcolor="#1565C0",
                    color="#FFFFFF",
                    width=220,
                ),
                ft.TextButton("Reset", on_click=on_reset),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

    page.update()

if __name__ == "__main__":
    ft.app(main)