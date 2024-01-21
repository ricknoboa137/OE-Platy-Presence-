import requests
import cv2
import base64
import numpy as np

# Define the IP address and port of the Flask application
HOST = 'localhost'  # Replace with the Flask application's IP address
PORT = 8228

# Create a request object for the live video stream
url = f'http://{HOST}:{PORT}/live_video.mp4'

# Continuously fetch the live video stream and decode the base64 data
while True:
    # Send a GET request for the live video stream
    response = requests.get(url).content

    # Decode the base64 data into a NumPy array
    decoded_data = base64.b64decode(response)

    # Convert the NumPy array to a frame
    frame = cv2.imdecode(np.frombuffer(decoded_data, dtype='uint8'), -1)

    # Display the frame
    cv2.imshow('Received Video', frame)

    # Check for the 'q' key to quit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Close the video stream
cv2.destroyAllWindows()