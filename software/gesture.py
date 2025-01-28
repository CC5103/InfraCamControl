# Description: This file contains the functions for gesture recognition.
import math

def calculate_angle(p1, p2, p3):
    """Calculates the angle between three points.

    Args:
        p1 (Point): The first point.
        p2 (Point): The second point.
        p3 (Point): The third point.
        
    Returns:
        float: The angle between the three points.
    """
    v1 = [p1.x - p2.x, p1.y - p2.y, p1.z - p2.z]
    v2 = [p3.x - p2.x, p3.y - p2.y, p3.z - p2.z]
    dot_product = sum(v1[i] * v2[i] for i in range(3))
    magnitude_v1 = math.sqrt(sum(v1[i] ** 2 for i in range(3)))
    magnitude_v2 = math.sqrt(sum(v2[i] ** 2 for i in range(3)))
    angle_rad = math.acos(dot_product / (magnitude_v1 * magnitude_v2))
    angle_deg = math.degrees(angle_rad)
    return angle_deg

def is_finger_straight(landmarks, finger_indices):
    """This function checks if a finger is straight.

    Args:
        landmarks (List[Point]): The list of landmarks.
        finger_indices (List[int]): The list of indices for the finger landmarks.
        
    Returns:
        bool: True if the finger is straight, False otherwise.
    """
    p1, p2, p3, p4 = [landmarks[i] for i in finger_indices]
    angle1 = calculate_angle(p1, p2, p3)
    angle2 = calculate_angle(p2, p3, p4)
    return abs(angle1 - 180) < 40 and abs(angle2 - 180) < 40

def recognize_gesture(landmarks):
    """This function recognizes the gesture based on the hand landmarks.

    Args:
        landmarks (List[Point]): The list of landmarks.

    Returns:
        str: The recognized gesture.
    """
    if len(landmarks) < 21:
        print("Incomplete hand landmarks, skipping gesture recognition.")
        return None

    thumb_straight = is_finger_straight(landmarks, [1, 2, 3, 4])
    index_straight = is_finger_straight(landmarks, [5, 6, 7, 8])
    middle_straight = is_finger_straight(landmarks, [9, 10, 11, 12])
    ring_straight = is_finger_straight(landmarks, [13, 14, 15, 16])
    pinky_straight = is_finger_straight(landmarks, [17, 18, 19, 20])

    Finger_up = landmarks[0].y < landmarks[17].y

    print(thumb_straight, index_straight, middle_straight, ring_straight, pinky_straight)
    if Finger_up:
        return None

    if not thumb_straight and not middle_straight and not ring_straight and not pinky_straight and index_straight: # 1
        return "0"
    elif not thumb_straight and not ring_straight and not pinky_straight and index_straight and middle_straight: # 2
        return "on"
    elif  not thumb_straight and not pinky_straight and index_straight and middle_straight and ring_straight: # 3
        return "off"
    elif thumb_straight and index_straight and middle_straight and ring_straight and pinky_straight: # 5
        return "start"
    else:
        return None
