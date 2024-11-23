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


def log_action(action, cluster, monitor):
    """Log action with location."""
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
    if len(prev_positions) == 0 or len(current_positions) == 0:
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


def detect_context_boundary(clusters, frame_width, frame_height):
    """Detect if clusters are near the screen's boundaries."""
    boundary_threshold = 0.1  # 10% of the screen's width/height
    move_camera = False
    camera_directions = []

    for cluster in clusters:
        cx, cy = cluster["center"]
        if cx < frame_width * boundary_threshold:
            move_camera = True
            camera_directions.append("left")
        elif cx > frame_width * (1 - boundary_threshold):
            move_camera = True
            camera_directions.append("right")
        if cy < frame_height * boundary_threshold:
            move_camera = True
            camera_directions.append("up")
        elif cy > frame_height * (1 - boundary_threshold):
            move_camera = True
            camera_directions.append("down")

    return move_camera, list(set(camera_directions))  # Avoid duplicate directions


def detect_new_context(prev_clusters, new_clusters):
    """Check if new clusters appear after camera movement."""
    prev_centers = {tuple(map(int, cluster["center"])) for cluster in prev_clusters}
    new_centers = {tuple(map(int, cluster["center"])) for cluster in new_clusters}

    new_context = new_centers - prev_centers
    return len(new_context) > 0, list(new_context)


def move_camera_if_needed(camera_directions, xcom_actions):
    """Move the camera in specified directions."""
    for direction in camera_directions:
        xcom_actions.rotate_camera(direction)
        print(f"Camera moved: {direction}")


def execute_actions(actions, xcom_actions, prev_positions, current_positions):
    """Execute actions using the XCOM2Actions class."""
    for action in set(actions):
        if validate_movement(action, prev_positions, current_positions):
            print(f"Action {action} validated successfully.")
        else:
            print(f"Action {action} failed validation. Retrying...")
            # Retry or handle failure as needed
        if action == "move_up":
            xcom_actions.move("up")
        elif action == "move_down":
            xcom_actions.move("down")
        elif action == "move_left":
            xcom_actions.move("left")
        elif action == "move_right":
            xcom_actions.move("right")


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

        # Cluster keypoints
        clusters = cluster_keypoints(keypoints)

        # Detect if camera movement is needed
        move_camera, directions = detect_context_boundary(
            clusters, monitor["width"], monitor["height"]
        )

        # Move camera if necessary
        if move_camera:
            move_camera_if_needed(directions, xc_actions())

        # Optical flow tracking
        if prev_gray is not None:
            new_points, prev_points = optical_flow_tracking(
                prev_gray, current_gray, prev_points
            )
        else:
            new_points, prev_points = None, None

        # Validate movement
        actions = determine_actions(clusters, monitor["width"], monitor["height"])
        execute_actions(actions, xc_actions(), prev_points, new_points)

        # Detect new context
        new_clusters = cluster_keypoints(keypoints)
        found_new_context, new_context = detect_new_context(clusters, new_clusters)
        if found_new_context:
            print(f"New context found: {new_context}")

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
