import json
import os
import tempfile
import uvicorn

from fastapi import FastAPI, File, UploadFile, HTTPException
import face_recognition
import cv2
import numpy as np

def load_references_images():
# Load a sample picture and learn how to recognize it.
    oren_image = face_recognition.load_image_file("./reference_image/oren0.jpg")
    oren_face_encoding = face_recognition.face_encodings(oren_image)[0]

    # # Load a second sample picture and learn how to recognize it.
    danyal_image = face_recognition.load_image_file("./reference_image/danyal0.jpg")
    danyal_face_encoding = face_recognition.face_encodings(danyal_image)[0]

    michael_image = face_recognition.load_image_file("./reference_image/michael0.jpg")
    michael_face_encoding = face_recognition.face_encodings(michael_image)[0]

    sam_image = face_recognition.load_image_file("./reference_image/sam0.jpg")
    sam_face_encoding = face_recognition.face_encodings(sam_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        oren_face_encoding,
        danyal_face_encoding,
        michael_face_encoding,
        sam_face_encoding 
    ]
    known_face_names = [
        "Oren",
        "Danyal",
        "Michael",
        "Sam"
    ]

    return (known_face_encodings,known_face_names)

known_face_encodings,known_face_names = load_references_images()

app: FastAPI = FastAPI()

@app.get("/api/ping")
def ping():
    return json.dumps({"PONG": True})

from gcloud import storage
# file.
storage_client = storage.Client.from_service_account_json(
    '/app/creds.json',"compiler-monkeys")

import pymongo
from dotenv import load_dotenv
load_dotenv()


db = pymongo.MongoClient(os.getenv("MONGO_URL")).face
collection = db.face

def upload_to_bucket(blob_name, path_to_file, bucket_name):
    """ Upload data to a bucket"""

    # Explicitly use service account credentials by specifying the private key

    #print(buckets = list(storage_client.list_buckets())

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)

    #returns a public url
    return blob.public_url

def upload_database(name:str, url:str):
    collection.insert_one({"name":name, "url": url})

async def predict( image: UploadFile = File(...)) -> str:
    contents = await image.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".jpg", delete=False) as FOUT:
        cv2.imwrite(FOUT.name,img)
        unknown_image = face_recognition.load_image_file(FOUT.name)
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            print(face_distances)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            link = upload_to_bucket(FOUT.name.split("/")[-1],FOUT.name,"face-rec123")
            upload_database(name,link)

            return name

    return ""

@app.post("/api/identifyguest")
async def identifyGuest( guest_photo: UploadFile = File(...)) -> str:
    extension = guest_photo.filename.split(".")[-1] in ("jpg","jpeg")

    if not extension:
        raise HTTPException(status_code=404, detail=".jpg and .jpeg file only")
    
    person_name = await predict(guest_photo)

    return person_name

    # if person_name != "" and person_name != "Michael":
    #     return True
    # else:
    #     return False


@app.get("/api/logs")
async def logs():
    logsArray = []
    for document in list(collection.find({})):
        try:
            docJson = {"name":document["name"], "url":document["url"]}
            logsArray.append(docJson)
        except:
            continue
    return logsArray

# if __name__ == "__main__":
uvicorn.run(app, host="0.0.0.0", port=8080)

