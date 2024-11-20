# backend/automation/screen_capture.py
import pyautogui


def capture_screen():
    screenshot = pyautogui.screenshot()
    screenshot.save("game_screen.png")
    return {"status": "Screenshot taken", "file": "game_screen.png"}
