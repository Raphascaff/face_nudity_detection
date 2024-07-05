from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
from nudenet import NudeDetector
from connect_database import execut_query
from query_console import get_user_url

app = FastAPI()

class UserImg(BaseModel):
    user_id: int


def get_image_from_url(image_url):
    """
    Provide the image from a public URL.
    """
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

def detect_nudity(image_data):
    """
    This function will receive the image and then check for possible nudity
    Returns a boolean
    """
    detector = NudeDetector()
    try:
        detections = detector.detect(image_data)
        detections = [item for item in detections if item['class'] != 'FACE_FEMALE']
        return len(detections) > 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def detect_face_in_image(image_data):
    """
    This function will receive the image and then check for possible face
    Returns a boolean
    """
    try:
        img_np = np.array(Image.open(BytesIO(image_data)))
        gray_img = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=4)
        return len(faces) > 0
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

@app.post("/detect-face/")
async def detect_face(image_url: UserImg):
    """
    It starts the API with a POST verb.
    The body shall contain the user id from your database 
    and will return the public url 
    Returns a contract with message and boole indicating whether it has nudity or/and face
    """
    url = execut_query(get_user_url(image_url.user_id))
    try:
        image_data = get_image_from_url(url)
        face_detected = detect_face_in_image(image_data)
        nudity_detected = detect_nudity(image_data)
        
        match (face_detected, nudity_detected):
            case (True, True):
                return {"face_detected": True, "nudity_detected": True, "message": "Both face and nudity were detected"}
            case (True, False):
                return {"face_detected": True, "nudity_detected": False, "message": "Face detected but nudity was not detected"}
            case (False, True):
                return {"face_detected": False, "nudity_detected": True, "message": "Nudity detected but face was not detected"}
            case (False, False):
                return {"face_detected": False, "nudity_detected": False, "message": "Neither face nor nudity were detected"}
            
    except SystemExit as e:
        raise HTTPException(status_code=400, detail=f"Error fetching image from URL: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)