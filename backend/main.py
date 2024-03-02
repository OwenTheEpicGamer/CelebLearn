"""
START EVERY THING WITH /api
MAKES CONNECTING THINGS LESS CONFUSING
"""

import dotenv
import os
import uvicorn
from fastapi import FastAPI, Request
import openai
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

dotenv.load_dotenv(".env")
print(os.getcwd())
openai.api_key = os.environ["OPENAI_API_KEY"]
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
    allow_headers=["*"]
)


# This is for inputs to directories, useless for now. Don't need for now
class Data(BaseModel):
    user: str


@app.get("/")
async def root():
    print("asdasd")
    return {"message": "Hello World"}


@app.post("/test")
async def test(req: Request):
    # print(data)
    data = await req.json()
    print(data)
    return {"data": "asdas"}


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
