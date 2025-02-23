import cv2
from picamera2 import Picamera2
import threading
import time
import json
from Sender import Sender_class
from signal_processing import save_thread
import cv2
import face_detection
import mediapipe as mp
import gesture as gesture

def fetch_slack_messages_thread(sender, last_timestamp, json_changed):
    """Fetch slack messages and send signal to IR LED.
    Args:
        sender (Sender_class): Sender class instance.
        last_timestamp (str): Last timestamp of fetched message.
        json_changed (bool): Flag for checking if json file is changed.    
    """
    while True:
        result = sender.fetch_slack_messages_with_retry(last_timestamp)
        if result:
            message, last_timestamp = result
            if message:
                print(f"Received message: {message}")
                if json_changed:
                    try:
                        with open("../IR_signal/signal_list.json") as f: # Load signal map from json file
                            signal_map = json.load(f)
                            json_changed = False
                    except FileNotFoundError:
                        print("Error: config.json not found")
                        exit(1)

                if message in signal_map:
                    sender.send_signal_wave(signal_map[message]) # Send signal to IR LED
                elif message.startswith("crate"):
                    try:
                        if message.split()[1] in ["0", "1"]:
                            save_thread(sender, signal_map, *message.split()[1:]) # Save signal to json file
                            json_changed = True
                        else:
                            sender.client.chat_postMessage(channel=sender.CHANNEL_ID, text=f"Invalid save_type: {message.split()[1]}. \nPlase input 0(NEC) or 1(MITSUBISHI).")
                    except IndexError:
                        sender.client.chat_postMessage(channel=sender.CHANNEL_ID, text=f"Invalid message: {message}. \nPlase input crate <save_type> <save_key> <save_name>.")
                else:
                    sender.client.chat_postMessage(channel=sender.CHANNEL_ID, text=f"Invalid message: {message}. \nPlase input {', '.join(list(signal_map.keys()))} \nor \ncrate <save_type> <save_key> <save_name>.")
                sender.first = True
                last_timestamp = None
        time.sleep(1)

def camera_thread(sender):
    """Capture video from camera and detect face using ultralight. And hand gesture using mediapipe.
    Args:
        sender (Sender_class): Sender class instance.
    """
    picam2 = Picamera2()
    
    video_config = picam2.create_video_configuration({"size": (640, 480)})
    picam2.configure(video_config)
    picam2.start()
    
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=1,
                           min_detection_confidence=0.5,
                           min_tracking_confidence=0.5)

    mp_draw = mp.solutions.drawing_utils
    
    try:
        with open("../IR_signal/signal_list.json") as f: # Load signal map from json file
            signal_map = json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found")
        exit(1)

    gesture_start_time = time.time() - 4 # Initialize gesture start time
    while True:
        frame = picam2.capture_array()
        flipped_frame = cv2.flip(frame, 0)

        # Face detection
        frame = face_detection.detect_first_face(flipped_frame)
        
        # Hand detection
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                # Gesture recognition
                gesture_message = gesture.recognize_gesture(hand_landmarks.landmark)
                # Send signal to IR LED
                if gesture_message:
                    if gesture_message == "start":
                        gesture_start_time = time.time()
                    elif time.time() - gesture_start_time < 4:
                        gesture_start_time  = gesture_start_time - 4
                        print(f"Received gesture: {gesture_message}")
                        sender.send_signal_wave(signal_map[gesture_message])

        cv2.imshow("Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # If the screen is black, turn on the infrared light
        # average_brightness = np.mean(gray)
        # if average_brightness < 20:
        #     sender.pi.write(sender.pin_sender, 1)
        # else:
        #     sender.pi.write(sender.pin_sender, 0)

    picam2.stop()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    sender = Sender_class()
    last_timestamp = None
    json_changed = True

    slack_thread = threading.Thread(target=fetch_slack_messages_thread, args=(sender, last_timestamp, json_changed))
    camera_thread = threading.Thread(target=camera_thread, args=(sender,))

    slack_thread.start()
    camera_thread.start()

    slack_thread.join()
    camera_thread.join()


