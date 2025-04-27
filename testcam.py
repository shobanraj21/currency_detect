import requests

# ESP32-CAM IP address
ESP32_CAM_IP = "http://192.168.0.6/capture"  # Replace <ESP32_IP> with your ESP32 IP

def get_image():
    try:
        print(f"Requesting image from {ESP32_CAM_IP}...")
        response = requests.get(ESP32_CAM_IP, timeout=10)

        if response.status_code == 200:
            with open('captured_from_esp32.jpg', 'wb') as f:
                f.write(response.content)
            print("Image saved as 'captured_from_esp32.jpg'")
        else:
            print(f"Failed to get image. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_image()
