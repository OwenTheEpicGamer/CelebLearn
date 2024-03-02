from openai import OpenAI
import os
import easyocr
import dotenv

dotenv.load_dotenv(".env")
openai_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)

reader = easyocr.Reader(["en"])
result = reader.readtext("image1.png")
summary = ""  # "chemistry is made of protons, neutrons, electrons, muons. it involves the study of macroscopic particles"

for bbox, text, prob in result:
    summary += text

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a tutor who takes a summary and turns it into a list a 5 key words to supplement the study method blurting",
        },
        {"role": "user", "content": summary},
    ],
)

keywords = []

items = completion.choices[0].message.content.split("\n")
for item in items:
    if item.strip():
        keywords.append((item.split(". ")[-1]))


audio_file = open("audio2.m4a", "rb")
transcript = client.audio.transcriptions.create(
    model="whisper-1", file=audio_file, response_format="json"
)

# transcript = "Input text: Protons, electrons, neutrons, muons are important."

# print(
# "Summary Text: chemistry is made of protons, neutrons, electrons, muons. it involves the study of macroscopic particles",
# )
print(transcript.text)
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
