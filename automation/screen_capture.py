import cv2
import numpy as np
import pyautogui


def capture_screen():
    # Capture the screen
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to a numpy array (required for OpenCV)
    frame = np.array(screenshot)

    # Convert RGB to BGR (OpenCV uses BGR format)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    return frame


def show_screen():
    # Capture the screen
    frame = capture_screen()

    # Display the captured screen in an OpenCV window
    cv2.imshow("Screen Capture", frame)

    # Wait for a key press and close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    show_screen()
