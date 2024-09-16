#MQTT IMAGE TRANSMISSION
import cv2
import threading
import time
import base64
from paho.mqtt import client as mqtt_client
import random


# Define the IP address and port for broadcasting
broker = '10.8.8.70'#'192.168.0.108'  # Broadcast to all devices on the network
port = 1883
topic = "test"


# Generate a Client ID with the publish prefix.
client_id = f'ImageProvider-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

################################################################################
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1,client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, msg):
    msg_count = 1
    #print(msg)
    result = client.publish(topic, msg) # result: [0, 1]
    status = result[0]
    if status == 0:
        msg_count += 1
        #print("Message Printed")
    else:
        print(f"Failed to send message to topic {topic}")
    
    
##################################################################################


client = connect_mqtt()
client.loop_start()
# Initialize the video capture object
cap = cv2.VideoCapture(0)  # 0 for the first webcam
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') #Load face detection model
# Set the frame rate to 30 frames per second
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(3, 1280)
cap.set(4, 480)
cont =1
while cont == 1:
    #cont =2
    # Read the current frame from the webcam
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    
    # Draw rectangle around the faces
    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"Face {i+1}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
    
    resize= cv2.resize(frame, (1280, 480))
    frame = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
    #print(frame.shape)
    res, frame = cv2.imencode('.jpg', frame)    # from image to binary buffer
    
    #print(frame)
    
    if not ret:
        break

    # Convert the frame to a Base64 array
    frame = base64.b64encode(frame) #frame.tobytes()
    
    # Send the encoded frame data as an Mqtt message
    publish(client, frame)

# Close the video capture object and video writer
client.loop_stop()
cap.release()

###################################################################################
