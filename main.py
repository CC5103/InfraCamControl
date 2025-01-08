# @Author: CC5103
# @Date: 2024/05/06

import threading
import time
import json
from Sender import Sender_class
from signal_processing import save_thread
import cv2
from picamera2 import Picamera2
import numpy as np

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
                        with open("signal_list.json") as f: # Load signal map from json file
                            signal_map = json.load(f)
                            json_changed = False
                    except FileNotFoundError:
                        print("Error: config.json not found")
                        exit(1)

                if message in signal_map:
                    sender.send_signal_wave(signal_map[message]) # Send signal to IR LED
                elif message.startswith("crate"):
                    save_thread(sender, signal_map, *message.split()[1:]) # Save signal to json file
                    json_changed = True
                else:
                    sender.client.chat_postMessage(channel=sender.CHANNEL_ID, text=f"Invalid message: {message}. \nPlase input {', '.join(list(signal_map.keys()))} \nor \ncrate <save_type> <save_key> <save_name>.")
                sender.first = True
                last_timestamp = None
        time.sleep(1)

def camera_thread(sender):
    """Capture video from camera and detect face.
    Args:
        sender (Sender_class): Sender class instance.
    """
    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration())
    picam2.start()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    while True:
        frame = picam2.capture_array()
        flipped_frame = cv2.flip(frame, 0)
        gray = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(flipped_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Face Detection", flipped_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # If the screen is black, turn on the infrared light
        average_brightness = np.mean(gray)
        if average_brightness < 20:
            sender.pi.write(sender.pin_sender, 1)
        else:
            sender.pi.write(sender.pin_sender, 0)

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
