import mss
import cv2
import numpy as np
import time

# live screen capture
sct = mss.mss()

# determine which screen to capture
monitor = sct.monitors[0]

# set screen for viewing feed
feed = sct.monitors[1]

# define monitor size & position
# smaller resolution for better fps
monitor = {"left": -2056, "top": 300, "width": 1920, "height": 1080}

# set feed position
feed = {"left": 0, "top": 0, "width": 960, "height": 540}


# for index, monitor in enumerate(sct.monitors):
#     print(f"screen {index}:{monitor}")
"""
  create a loop that takes screen shots, converts the color
  to rgb then display the image, exit w/ 'q'
"""
try:
    while True:
        # capture frame
        frame = np.array(sct.grab(monitor))
        # convert to rgb
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        # resize frame for feed
        mini_frame = cv2.resize(frame, (feed["width"], feed["height"]))
        # display frame
        cv2.imshow("live frame feed", mini_frame)
        # move window
        cv2.moveWindow("live frame feed", feed["left"], feed["top"])
        # exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    print("Feed ended: User")

finally:
    cv2.destroyAllWindows()
