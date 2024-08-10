from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from connect_database import execut_query
from query_console import get_user_url
from nudity_face_controller import get_image_from_url, detect_face_in_image, detect_nudity, face_controller

app = FastAPI()

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

