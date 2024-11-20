# backend/automation/api_client.py
import requests


def send_action(action, x, y):
    url = "http://127.0.0.1:8000/perform_action/"
    data = {"action": action, "x": x, "y": y}
    response = requests.post(url, json=data)
    return response.json()
