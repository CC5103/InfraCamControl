from ultralytics import YOLO
import cv2
from picamera2 import Picamera2
import threading
import time
import json
from Sender import Sender_class
from signal_processing import save_thread
import cv2

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
                    if message.split()[1] in [0, 1]:
                        save_thread(sender, signal_map, *message.split()[1:]) # Save signal to json file
                        json_changed = True
                    else:
                        sender.client.chat_postMessage(channel=sender.CHANNEL_ID, text=f"Invalid save_type: {message.split()[1]}. \nPlase input 0(NEC) or 1(MITSUBISHI).")
                else:
                    sender.client.chat_postMessage(channel=sender.CHANNEL_ID, text=f"Invalid message: {message}. \nPlase input {', '.join(list(signal_map.keys()))} \nor \ncrate <save_type> <save_key> <save_name>.")
                sender.first = True
                last_timestamp = None
        time.sleep(1)

def camera_thread(sender):
    """ Camera thread for face detection using YOLO.  
    Args:
        sender (Sender_class): Sender class instance.
    """
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration({"size": (640, 480)})
    picam2.configure(video_config)
    picam2.start()

    model = YOLO("yolov8n.pt")

    while True:
        frame = picam2.capture_array()
        flipped_frame = cv2.flip(frame, 0)
        frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGRA2BGR)

        results = model.predict(frame, conf=0.5, classes=0, device="cpu", verbose=False)

        for result in results:
            if len(result.boxes) > 0:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = box.conf[0]

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"Face {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv2.imshow("YOLO Face Detection", frame)

        # If the screen is black, turn on the infrared light
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # if np.mean(gray) < 20:
        #     sender.pi.write(sender.pin_sender, 1)
        # else:
        #     sender.pi.write(sender.pin_sender, 0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

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


