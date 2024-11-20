# backend/api/action.py
import pyautogui


def perform_click(x, y):
    pyautogui.click(x, y)
    return {"status": "Click action performed", "coordinates": {"x": x, "y": y}}


def perform_move(x, y):
    pyautogui.moveTo(x, y)
    return {"status": "Move action performed", "coordinates": {"x": x, "y": y}}
