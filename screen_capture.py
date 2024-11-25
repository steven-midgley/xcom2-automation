import cv2
import numpy as np
from mss import mss

def capture_screen(region=None):
    with mss() as sct:
        monitor = sct.monitors[1]  # Capture the primary monitor
        if region:
            monitor = region
        screenshot = np.array(sct.grab(monitor))
        return cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)