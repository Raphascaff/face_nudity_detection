# face_nudity_detection
This API is intended to Identity images with nudity content and a human face, returning a full functional contract.
Using FastAPI I`m providing a endpoint with POST Verb where the user will connect to their database and get the url with the user image.
Once having the url containing the image, the API will test the and return if it has face and/or nudity.

To run the API go to your console and use the following command: uvicorn main:app --reload

Once it is running, go to your browse and past the provided HTTPS address, followed by /docs. This will start a Swagger page, use the try-out function
Have fun!
