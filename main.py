import mss
import cv2
import numpy as np
import time

# Initialize mss and ORB for feature detection
sct = mss.mss()
orb = cv2.ORB_create()

# Define monitor for screen capture
monitor = {"left": -1728, "top": 120, "width": 1728, "height": 1115}

# Set feed position for displaying processed frame
feed = {"left": 0, "top": 0, "width": 960, "height": 540}

# Load templates for feature matching (e.g., troop icons, objectives)
# Example: Precompute ORB descriptors for templates
templates = [
    {"name": "troop", "image": "troop_icon.png"},
    {"name": "objective", "image": "objective_icon.png"},
]
for template in templates:
    img = cv2.imread(template["image"], cv2.IMREAD_GRAYSCALE)
    template["keypoints"], template["descriptors"] = orb.detectAndCompute(img, None)


# Helper function to detect features in the global frame
def detect_features(frame, templates):
    detected = []
    keypoints, descriptors = orb.detectAndCompute(frame, None)
    for template in templates:
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = matcher.match(template["descriptors"], descriptors)
        if matches:
            detected.append({"name": template["name"], "matches": matches})
    return detected


# Main loop
try:
    while True:
        # Capture the current frame
        frame = np.array(sct.grab(monitor))
        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

        # Detect features in the frame
        detected_features = detect_features(grey_frame, templates)

        # Summarize global state
        global_state = {
            "phase": "Command",  # Static placeholder for now
            "features": detected_features,
        }

        # Debugging: Display detected features and global state
        for feature in detected_features:
            print(f"Detected: {feature['name']} with {len(feature['matches'])} matches")

        # Generate a debug overlay
        debug_frame = grey_frame.copy()
        for feature in detected_features:
            for match in feature["matches"]:
                pt = orb.detect(grey_frame, None)[match.trainIdx].pt
                cv2.circle(debug_frame, (int(pt[0]), int(pt[1])), 5, (0, 255, 0), -1)

        # Resize for display
        mini_frame = cv2.resize(debug_frame, (feed["width"], feed["height"]))

        # Display debug information
        cv2.putText(
            mini_frame,
            f"Features Detected: {len(detected_features)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
        cv2.imshow("Live Frame Feed", mini_frame)
        cv2.moveWindow("Live Frame Feed", feed["left"], feed["top"])

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    print("Feed ended: User")

finally:
    cv2.destroyAllWindows()
