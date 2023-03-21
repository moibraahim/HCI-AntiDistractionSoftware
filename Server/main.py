import cv2
import mediapipe as mp
import socket
import numpy as np

HOST = '127.0.0.1'  # IP address of the Python script
PORT = 8080  # Choose a port number that is not currently in use

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)

# Accept a connection from a client
print("Waiting for a client to connect...")
client_socket, client_address = server_socket.accept()
print("Connected by", client_address)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)


data = ""
with mp_hands.Hands(
    model_complexity=0,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Send the finger landmarks over the socket connection
                flattened_landmarks = [int(point.x * 1000) for point in hand_landmarks.landmark] + \
                                      [int(point.y * 1000) for point in hand_landmarks.landmark]


                # Generate the flattened_landmarks array
                flattened_landmarks = [f'{x:d}' for x in flattened_landmarks]
                flattened_landmarks_str = ','.join(flattened_landmarks).encode('utf-8')
                print(flattened_landmarks_str)

                client_socket.sendall(flattened_landmarks_str)

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        k = cv2.waitKey(1)
        if k % 256 == 27 or k == ord('q'):
            break

# Clean up
client_socket.close()
server_socket.close()
cap.release()
cv2.destroyAllWindows()
