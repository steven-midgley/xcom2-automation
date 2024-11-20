# /scripts/setup.py
from setuptools import setup

setup(
    name="xcom2-automation",
    version="0.1",
    install_requires=[
        "opencv-python",
        "pytesseract",
        "stable-baselines3",
        "pyautogui",
        "tensorflow",
        "gymnasium",
        "pillow",
        "fastapi",
        "uvicorn",
    ],
)
