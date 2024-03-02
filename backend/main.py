"""
START EVERY THING WITH /api
MAKES CONNECTING THINGS LESS CONFUSING
"""

import dotenv
import os
import uvicorn
from fastapi import FastAPI, Request
import openai
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import PyPDF2

dotenv.load_dotenv(".env")
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=openai.api_key)
MODEL = "gpt-3.5-turbo"

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
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


@app.get("/api/keywords")
async def generate_keywords():
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
    keywords = [item.split(". ")[-1] for item in items if item.strip()]
    return {"keywords": keywords}


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
