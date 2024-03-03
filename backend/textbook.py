from openai import OpenAI
import os
import dotenv
import PyPDF2
from pathlib import Path
from openai import OpenAI
import requests


client = OpenAI()


dotenv.load_dotenv(".env")
openai_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)


# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


pdf_path = "backend/assets/celeb.pdf"
extracted_text = extract_text_from_pdf(pdf_path)

# Takes text from PDF and turns it into a summary
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
speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=summary,
)

response.stream_to_file(speech_file_path)

# Turns everything into 5 keywords

person = "obama"

completion2 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": (
                "You are ",
                person,
                "tutoring who takes a summary and turns it into 5 keywords",
            ),
        },
        {"role": "user", "content": summary},
    ],
)

items = completion2.choices[0].message.content.split("\n")
keywords = []
for item in items:
    if item.strip():
        keywords.append((item.split(". ")[-1]))

audio_file = open("backend/assets/audio3.m4a", "rb")
transcript = client.audio.transcriptions.create(
    model="whisper-1", file=audio_file, response_format="json"
)

print("Summary: ", summary)
print("Transcript: ", transcript.text)
count = 0

for x in keywords:
    if transcript.text.lower().__contains__(x.lower()):
        count += 1
    else:
        print("Missing: " + x)

print(count, "/", len(keywords))
print("List of Keywords:")
for x in keywords:
    print(x)
