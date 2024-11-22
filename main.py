import cv2
import numpy as np
import mss
import logging
from xcom_actions.key_bindings import XCOM2Actions as xc_actions

# Initialize mss for screen capture
sct = mss.mss()

# Monitor region: adjust for your screen/game location
monitor = {"left": -1728, "top": 120, "width": 1728, "height": 1115}

# ORB and optical flow initialization
orb = cv2.ORB_create(nfeatures=1000)
lk_params = dict(
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
)

# Variables for tracking keypoints and clusters
prev_gray = None
prev_points = None
clusters = []


def log_action(action, cluster, monitor):
    cx, cy = cluster["center"]
    frame_x = monitor["left"] + cx
    frame_y = monitor["top"] + cy
    logging.info(f"Action: {action} at ({frame_x}, {frame_y})")


def process_frame(frame):
    """Process frame to extract keypoints and descriptors."""
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
    kp, des = orb.detectAndCompute(gray_frame, None)
    return gray_frame, kp, des


def cluster_keypoints(keypoints, threshold=30):
    """Cluster keypoints based on spatial proximity."""
    clusters = []
    for kp in keypoints:
        added = False
        for cluster in clusters:
            if (
                np.linalg.norm(np.array(cluster["center"]) - np.array(kp.pt))
                < threshold
            ):
                cluster["points"].append(kp)
                cluster["center"] = np.mean([p.pt for p in cluster["points"]], axis=0)
                added = True
                break
        if not added:
            clusters.append({"points": [kp], "center": kp.pt})
    return clusters


def determine_actions(clusters, frame_width, frame_height):
    """Determine logical actions based on cluster positions."""
    actions = []
    for cluster in clusters:
        cx, cy = cluster["center"]
        if cy < frame_height * 0.3:
            actions.append("move_up")
        elif cy > frame_height * 0.7:
            actions.append("move_down")
        if cx < frame_width * 0.3:
            actions.append("move_left")
        elif cx > frame_width * 0.7:
            actions.append("move_right")
    return actions


def validate_movement(expected_direction, prev_positions, current_positions):
    """Validate movement by comparing previous and current positions."""
    if prev_positions is None or current_positions is None:
        return False

    movement_vector = np.mean(current_positions, axis=0) - np.mean(
        prev_positions, axis=0
    )
    direction_map = {
        "move_up": (0, -1),
        "move_down": (0, 1),
        "move_left": (-1, 0),
        "move_right": (1, 0),
    }
    expected_vector = np.array(direction_map[expected_direction])

    # Normalize and compare vectors
    if np.linalg.norm(movement_vector) == 0:
        return False
    actual_vector = movement_vector / np.linalg.norm(movement_vector)
    similarity = np.dot(actual_vector, expected_vector)

    # If similarity is close to 1, movement is validated
    return similarity > 0.8


def execute_actions(actions, xcom_actions, prev_positions, current_positions):
    """Execute actions using the XCOM2Actions class."""
    for action, cluster in zip(set(actions), clusters):
        kx, ky = cluster["center"]
        frame_x = monitor["left"] + kx
        frame_y = monitor["top"] + ky
        if action == "move_up":
            xcom_actions.move("up")
            print(f"Action: move_up at ({frame_x}, {frame_y})")
        elif action == "move_down":
            xcom_actions.move("down")
            print(f"Action: move_down at ({frame_x}, {frame_y})")
        elif action == "move_left":
            xcom_actions.move("left")
            print(f"Action: move_left at ({frame_x}, {frame_y})")
        elif action == "move_right":
            xcom_actions.move("right")
            print(f"Action: move_right at ({frame_x}, {frame_y})")
        # Validate movement
        if validate_movement(action, prev_positions, current_positions):
            print(f"Action {action} validated successfully.")
        else:
            print(f"Action {action} failed validation. Retrying...")
            # Retry or handle failure as needed


def optical_flow_tracking(prev_gray, current_gray, prev_points):
    """Track keypoints with optical flow."""
    if prev_points is not None and len(prev_points) > 0:
        new_points, st, err = cv2.calcOpticalFlowPyrLK(
            prev_gray, current_gray, prev_points, None, **lk_params
        )
        valid_new_points = new_points[st == 1]
        valid_prev_points = prev_points[st == 1]
        return valid_new_points, valid_prev_points
    return None, None


# Main loop
try:
    while True:
        # Capture the screen
        screen = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)

        # Process frame for keypoints and descriptors
        current_gray, keypoints, descriptors = process_frame(frame)

        # Validate frame size and points
        if prev_gray is None or prev_gray.shape != current_gray.shape:
            prev_gray = current_gray
            prev_points = np.array(
                [kp.pt for kp in keypoints], dtype=np.float32
            ).reshape(-1, 1, 2)
            continue

        # Optical flow tracking
        new_points, prev_points = optical_flow_tracking(
            prev_gray, current_gray, prev_points
        )
        if new_points is not None:
            for p in new_points:
                x, y = p.ravel()
                cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 0), -1)

        # Visualize clusters
        for cluster in clusters:
            cx, cy = map(int, cluster["center"])
            frame_x = monitor["left"] + cx
            frame_y = monitor["top"] + cy
            cv2.putText(
                frame,
                f"({frame_x}, {frame_y})",
                (cx, cy),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 0),
                1,
            )
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        # Cluster keypoints
        clusters = cluster_keypoints(keypoints)

        # Determine actions
        actions = determine_actions(clusters, monitor["width"], monitor["height"])
        execute_actions(actions, xc_actions(), prev_points, new_points)
        logging.basicConfig(filename="xcom_actions.log", level=logging.INFO)

        # Display the frame
        cv2.imshow("XCOM2 Automation", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # Update previous frame and points
        prev_gray = current_gray.copy()
        prev_points = np.array([kp.pt for kp in keypoints], dtype=np.float32).reshape(
            -1, 1, 2
        )


except KeyboardInterrupt:
    print("Automation interrupted.")

finally:
    cv2.destroyAllWindows()
