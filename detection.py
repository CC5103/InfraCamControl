import time
import gesture

class Detection():
    def __init__(self, sender, mp_face_mesh, face_mesh, mp_hands, hands, mp_draw, draw_spec, signal_map):
        """Initialize detection class.
        
        Args:
            sender (Sender_class): Sender class instance.
            mp_face_mesh (mediapipe class): Mediapipe
            face_mesh (mediapipe class): Mediapipe
            mp_hands (mediapipe class): Mediapipe
            hands (mediapipe class): Mediapipe
            mp_draw (mediapipe class): Mediapipe
            draw_spec (mediapipe class): Mediapipe
            signal_map (dict): Signal map.
        """
        self.sender = sender
        self.mp_face_mesh = mp_face_mesh
        self.face_mesh = face_mesh
        self.mp_hands = mp_hands
        self.hands = hands
        self.mp_draw = mp_draw
        self.draw_spec = draw_spec
        self.signal_map = signal_map

    def face_detection(self, frame):
        """Face detection using mediapipe.

        Args:
            frame (np.array): Image frame.
        """
        face_results = self.face_mesh.process(frame)
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                self.mp_draw.draw_landmarks(frame, face_landmarks, connections=self.mp_face_mesh.FACEMESH_TESSELATION, landmark_drawing_spec=self.draw_spec, connection_drawing_spec=self.draw_spec)

    def hand_detectiont(self, frame_copy, frame, gesture_start_time, start_bool):
        """fast hand detection using mediapipe.
        
        Args:
            frame_copy (np.array): Image frame.
            frame (np.array): Image frame. But this is used for drawing.
            gesture_start_time (float): Gesture start time.
            start_bool (bool): Start bool.
        """
        results_precise = self.hands.process(frame_copy)
        if results_precise.multi_hand_landmarks:
            for hand_landmarks in results_precise.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                # Gesture recognition
                gesture_message = gesture.recognize_gesture(hand_landmarks.landmark)
                # Gesture start
                if gesture_message:
                    if gesture_message == "start":
                        gesture_start_time = time.time()
                        self.sender.pi.write(self.sender.pin_hand, 1)
                        start_bool = True
                    elif time.time() - gesture_start_time < 4:
                        gesture_start_time  = gesture_start_time - 4
                        # Send signal to IR LED
                        print(f"Received gesture: {gesture_message}")
                        self.sender.send_signal_wave(self.signal_map[gesture_message])

        if time.time() - gesture_start_time > 4 and start_bool:
            print("Gesture timeout")
            self.sender.pi.write(self.sender.pin_hand, 0)
            start_bool = False

        return gesture_start_time, start_bool, frame
    
if __name__ == '__main__':
    pass