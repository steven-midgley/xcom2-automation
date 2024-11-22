import mss
import cv2
import numpy as np
import time

# initiate mss
sct = mss.mss()

# determine which screen to capture
monitor = sct.monitors[0]
print(monitor)
# create variable
previous_frame = None

# set screen for viewing feed
feed = sct.monitors[1]

# define monitor size & position
# smaller resolution for better fps
monitor = {
    "left": -1728,
    "top": 120,
    "width": 1728,
    "height": 1115,
}

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
        # convert to gray scale
        frame = np.array(sct.grab(monitor))
        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

        # check for previous_frame
        if previous_frame is not None:
            # calculate dense flow
            flow = cv2.calcOpticalFlowFarneback(
                previous_frame,
                grey_frame,
                None,
                pyr_scale=0.0,  # More sensitivity to smaller motions
                levels=6,  # Multi-scale motion detection
                winsize=5,  # Smaller window for finer details
                iterations=10,  # Increased iterations for accuracy
                poly_n=5,  # Fine motion capture
                poly_sigma=1.5,  # Sharper detection
                flags=0,  # Default
            )

            # detect magnitude
            magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            # hsv settings
            hsv = np.zeros(
                (grey_frame.shape[0], grey_frame.shape[1], 3), dtype=np.uint8
            )
            hsv[..., 1] = 126  # saturation
            hsv[..., 0] = angle * 180 / np.pi / 2  # directional effects on hue
            hsv[..., 2] = cv2.normalize(
                magnitude, None, 0, 255, cv2.NORM_MINMAX
            )  # normalize values

            # flow feed
            flow_feed = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

            # resize frame for feed
            # display frame
            # move window
            mini_frame = cv2.resize(flow_feed, (feed["width"], feed["height"]))
            cv2.imshow("live frame feed", mini_frame)
            cv2.moveWindow("live frame feed", feed["left"], feed["top"])

        # update previous_frame
        previous_frame = grey_frame

        # exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    print("Feed ended: User")

finally:
    cv2.destroyAllWindows()
