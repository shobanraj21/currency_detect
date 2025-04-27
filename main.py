from flask import Flask, request, jsonify ,render_template
from ultralytics import YOLO
import os
import aiocoap
import asyncio
from threading import Thread
import time
import requests

app = Flask(__name__)

def detect(file):
    model = YOLO("best.pt")
    results = model.predict(file, conf=0.9)
    result = results[0]
    try:
        len(result.boxes)
        box = result.boxes[0]
        class_id = result.names[box.cls[0].item()]
        currency = class_id 
    except:
        print("No object detected")
        currency = 0
    return currency

def fetch_image():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def fetch():
        protocol = await aiocoap.Context.create_client_context()
        request = aiocoap.Message(code=aiocoap.GET, uri="coap://device_ip/get_image")
        try:
            response = await protocol.request(request).response
            with open("received_image.jpg", "wb") as f:
                f.write(response.payload)
        except Exception as e:
            print(f"Error fetching image: {e}")

    loop.run_until_complete(fetch())

#initializing the camera page
@app.route('/', methods = ['GET'])
def index():

    return render_template('index.html')

def get_image():
    try:
        url = "http://device_ip/get_image"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open("received_image.jpg", "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
        else:
            print(f"Failed to fetch image. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching image: {e}")

@app.route('/detect', methods = ['POST' ,'GET'])
def detect_currency(): 

    thread = Thread(target=fetch_image)
    thread.start()
    thread.join()
    image = "received_image.jpg"
    if not os.path.exists(image):
        return None
    currency = detect(image)

    return jsonify({'currency': currency})

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)