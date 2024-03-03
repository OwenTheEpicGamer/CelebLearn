"""
START EVERY THING WITH /api
MAKES CONNECTING THINGS LESS CONFUSING
"""
from rvc_python.infer import infer_file, infer_files
import os
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi import UploadFile
import openai
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import PyPDF2
from starlette.responses import JSONResponse
from openai import OpenAI
import os
import dotenv
import PyPDF2
from pathlib import Path
from openai import OpenAI
import os
import dropbox.files
import requests
import dotenv

dotenv.load_dotenv(".env")
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=openai.api_key)
MODEL = "gpt-3.5-turbo"

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://localhost:3001",
    "localhost:3001",
]

"""In order to make cross-origin requests -- i.e., requests that originate from a different protocol, IP address, 
domain name, or port -- you need to enable Cross Origin Resource Sharing (CORS)."""
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# This is for inputs to directories, useless for now. Don't need for now
class Data(BaseModel):
    user: str


@app.get("/")
async def root():
    print("asdasd")
    return {"message": "Hello World"}


@app.post("/api/test")
async def test(req: Request):
    # print(data)
    data = await req.json()
    print(data)
    return {"data": "asdas"}


@app.post("/api/upload")
async def upload_file(file: UploadFile = Form(...), character: str = Form(...)):
    global requests
    if not file:
        return JSONResponse(status_code=400, content={"message": False})

    print("Character: " + character)

    with open("./assets/uploaded_file.pdf", "wb") as buffer:
        buffer.write(await file.read())
        print("File uploaded and written")
    extracted_text = extract_text_from_pdf("./assets/uploaded_file.pdf")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a tutor who takes a textbook and summarizes it in 50 words",
            },
            {"role": "user", "content": extracted_text},
        ],
    )

    summary = completion.choices[0].message.content

    # Input summary, turns it into a mp3 file
    speech_file_path = Path(__file__).parent / "./videoaudio/speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=summary,
    )
    response.stream_to_file(speech_file_path)

    # Processing everything into OBAMAS voice
    result = infer_file(
        input_path="./videoaudio/speech.mp3",
        model_path=f"./model/{character}/model.pth",
        index_path="",  # Optional: specify path to index file if available
        device="cpu:0",  # Use cpu or cuda
        f0method="harvest",  # Choose between 'harvest', 'crepe', 'rmvpe', 'pm'
        # Transpose setting
        # Output file path
        index_rate=0.5,
        filter_radius=3,
        resample_sr=0,  # Set to desired sample rate or 0 for no resampling.
        rms_mix_rate=0.25,
        protect=0.33,
        version="v2"
    )

    """"""

    dotenv.load_dotenv(".env")

    dbx = dropbox.Dropbox(os.environ["DROPBOX_KEY"])

    def upload_all_local_files(character):
        for file in os.listdir("./videoaudio"):
            with open(os.path.join("./videoaudio", file), "rb") as f:
                if f.name.endswith(".mp4") and f.name.__contains__(character):
                    data = f.read()
                    dbx.files_upload(data, f"/video.mp4")
                elif f.name.endswith(".mp3"):
                    data = f.read()
                    dbx.files_upload(data, f"/audio.mp3")
                else:
                    continue

    upload_all_local_files(character)

    access_token = os.environ["DROPBOX_KEY"]

    url = "https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    data = {
        "path": "/audio.mp3",
        "settings": {
            "access": "viewer",
            "allow_download": True,
            "audience": "public",
            "requested_visibility": "public",
        },
    }

    response1 = requests.post(url, headers=headers, json=data)
    response_data = response1.json()
    url = response_data["url"]

    index_of_com = url.find(".com")
    after_com = url[index_of_com + len(".com"):]
    new_link = "https://dl.dropboxusercontent.com" + after_com

    url = "https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    data = {
        "path": "/video.mp4",
        "settings": {
            "access": "viewer",
            "allow_download": True,
            "audience": "public",
            "requested_visibility": "public",
        },
    }

    response2 = requests.post(url, headers=headers, json=data)
    response_data2 = response2.json()
    url = response_data2["url"]

    index_of_com = url.find(".com")
    after_com = url[index_of_com + len(".com"):]
    new_link2 = "https://dl.dropboxusercontent.com" + after_com
    print(new_link)

    """
    """

    url = "https://api.synclabs.so/video"

    payload = {
        "audioUrl": f"{new_link}",
        "maxCredits": 5000,
        "model": "wav2lip++",
        "synergize": True,
        "videoUrl": f"{new_link2}",
    }
    headers = {
        "x-api-key": "4e2ba9af-22ca-4c5b-9c0d-8061f3fe4213",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)

    while True:
        url = f"https://api.synclabs.so/video/{response.json()['id']}"

        headers = {
            "x-api-key": "4e2ba9af-22ca-4c5b-9c0d-8061f3fe4213",
            "Content-Type": "application/json"
        }

        response = requests.request("GET", url, headers=headers)

        if response.json()["status"] == "COMPLETED":
            print(response.json()['status'])
            break

    file_url = response.json()['url']
    print(file_url)

    file_path = "../frontend/public/url.txt"

    # Open the file in write mode ('w')
    with open(file_path, "w") as file:
        file.write(file_url)

    return {"filename": file.name, "text": character, "msg": 200, "url": file_url}


@app.post("/api/upload_audio")
async def upload_audio(audio: UploadFile):
    if not audio.filename.endswith(".mp3"):
        return JSONResponse(status_code=400, content={"message": "Unsupported file format"})

    with open(audio.filename, "wb") as buffer:
        buffer.write(await audio.read())

    return {"message": "Audio uploaded successfully"}


@app.post("/api/video")
async def lipsync():
    url = "https://api.synclabs.so/video/obama"
    headers = {"x-api-key": "4e2ba9af-22ca-4c5b-9c0d-8061f3fe4213"}
    response = requests.request("GET", url, headers=headers)
    print(response.text)


@app.get("/api/summary")
async def generate_summary():
    pdf_path = "backend/assets/celeb.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a tutor who takes a textbook and summarizes it in 50 words",
            },
            {"role": "user", "content": extracted_text},
        ],
    )
    summary = completion.choices[0].message.content
    return {"summary": summary}


@app.post('/api/webhook')
async def webhook():
    pass


@app.get("/api/keywords")
async def generate_keywords():
    pdf_path = "./assets/uploaded_file.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a tutor who takes a textbook and summarizes it in 50 words",
            },
            {"role": "user", "content": extracted_text},
        ],
    )
    summary = completion.choices[0].message.content
    completion2 = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a tutor who takes a summary and turns it into 5 keywords",
            },
            {"role": "user", "content": summary},
        ],
    )
    items = completion2.choices[0].message.content.split("\n")
    phrases = [item.split(". ")[-1] for item in items if item.strip()]
    keywords = []

    for phrase in phrases:
        keywords.extend(phrase.split())
    return {"keywords": keywords}


# when opening the audio player call the openai api instantly and wait


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
