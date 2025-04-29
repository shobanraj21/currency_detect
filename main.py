from flask import Flask, request, jsonify ,render_template
from ultralytics import YOLO
import os
import aiocoap
import asyncio
from threading import Thread
import time
import requests

ESP32_CAM_IP = "http://192.168.0.5/capture"  # Replace <ESP32_IP> with your ESP32 IP

app = Flask(__name__)

def detect(file):
    model = YOLO("best.pt")
    results = model.predict(file, conf=0.7)
    result = results[0]
    try:
        len(result.boxes)
        box = result.boxes[0]
        class_id = result.names[box.cls[0].item()]
        currency = class_id 
        print("currency:", currency)
    except:
        print("No object detected")
        currency = 0
    return currency


#initializing the camera page
@app.route('/', methods = ['GET'])
def index():

    return render_template('index.html')

def get_image():
    try:
        print(f"Requesting image from {ESP32_CAM_IP}...")
        response = requests.get(ESP32_CAM_IP, timeout=10)

        if response.status_code == 200:
            with open('received_image.jpg', 'wb') as f:
                f.write(response.content)
            print("Image saved as 'received_image.jpg'")
        else:
            print(f"Failed to get image. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/detect', methods = ['POST' ,'GET'])
def detect_currency(): 

    thread = Thread(target=get_image)
    thread.start()
    thread.join()
    image = "received_image.jpg"
    if not os.path.exists(image):
        return None
    currency = detect(image)

    return jsonify({'currency': currency})

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)