import requests
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
from nudenet import NudeDetector

def get_image_from_url(image_url):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
def detect_nudity(image_data):
    detector = NudeDetector()
    try:
        detections = detector.detect(image_data)
        detections = [item for item in detections if item['class'] != 'FACE_FEMALE']
        return len(detections) > 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def detect_face_in_image(image_data):

    try:
        img_np = np.array(Image.open(BytesIO(image_data)))
        gray_img = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=4)
        return len(faces) > 0
    except Exception as e:
        print(f"Error processing image: {e}")
        return False