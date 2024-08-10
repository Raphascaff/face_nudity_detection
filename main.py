from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from connect_database import execut_query
from query_console import get_user_url
from nudity_face_controller import get_image_from_url, detect_face_in_image, detect_nudity

app = FastAPI()

def face_controller(face_detected, nudity_detected):
    match (face_detected, nudity_detected):
        case (True, True):
            return {"face_detected": True, "nudity_detected": True, "message": "Both face and nudity were detected"}
        case (True, False):
            return {"face_detected": True, "nudity_detected": False, "message": "Face detected but nudity was not detected"}
        case (False, True):
            return {"face_detected": False, "nudity_detected": True, "message": "Nudity detected but face was not detected"}
        case (False, False):
            return {"face_detected": False, "nudity_detected": False, "message": "Neither face nor nudity were detected"}

class UserImg(BaseModel):
    user_id: int

@app.post("/detect-face/")
async def detect_face(image_url: UserImg):
    url = execut_query(get_user_url(image_url.user_id))
    try:
        image_data = get_image_from_url(url)
        face_detected = detect_face_in_image(image_data)
        nudity_detected = detect_nudity(image_data)
        return face_controller(face_detected, nudity_detected)
    except SystemExit as e:
        raise HTTPException(status_code=400, detail=f"Error fetching image from URL: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

