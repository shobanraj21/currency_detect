import camera
import network
import socket
import time

# Wi-Fi credentials
SSID = 'Rogue one'
PASSWORD = 'twaseem28'

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)
    print("Connected:", wlan.ifconfig())

# Initialize camera
def init_camera():
    try:
        camera.deinit()  # In case it was already initialized
        camera.init(0, format=camera.JPEG)
        print("Camera initialized")
    except Exception as e:
        print("Camera init failed:", e)

# Capture image
def capture_image():
    try:
        buf = camera.capture()
        if buf:
            print(f"Captured image size: {len(buf)} bytes")
            return buf
        else:
            print("Capture returned None")
            return None
    except Exception as e:
        print("Capture failed:", e)
        return None

# Start HTTP server
def start_http_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Listening on", addr)

    while True:
        try:
            cl, addr = s.accept()
            print('Client connected from', addr)
            request = cl.recv(1024)
            request = str(request)
            print("Request:", request)

            if 'GET /capture' in request:
                print("Capture requested")
                image = capture_image()
                if image:
                    cl.send(b"HTTP/1.1 200 OK\r\n")
                    cl.send(b"Content-Type: image/jpeg\r\n")
                    cl.send(b"Content-Length: " + str(len(image)).encode() + b"\r\n")
                    cl.send(b"Connection: close\r\n")
                    cl.send(b"\r\n")
                    cl.sendall(image)
                else:
                    cl.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\nCapture failed")
            else:
                cl.send(b"HTTP/1.1 404 Not Found\r\n\r\nPage not found")

            cl.close()
            print("Connection closed")
            time.sleep(0.2)  # Prevent CPU overuse

        except Exception as e:
            print("Socket error:", e)

# Main
try:
    connect_wifi()
    init_camera()
    start_http_server()
except Exception as e:
    print("An error occurred:", e)
finally:
    camera.deinit()

