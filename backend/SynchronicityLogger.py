import requests

url = "https://api.synclabs.so/video"

payload = {
    "audioUrl": "https://drive.google.com/file/d/1FvPblbdPc0_rXliiszsqd9iQHOQjcAQi/view?usp=sharing",
    "maxCredits": 123,
    "model": "wav2lip++",
    "synergize": True,
    "videoUrl": "https://drive.google.com/file/d/1VhEa81-XqYv5RDehvkwVVEAggLqLN0iP/view?usp=sharing",
    "webhookUrl": "",
}
headers = {
    "x-api-key": "4e2ba9af-22ca-4c5b-9c0d-8061f3fe4213",
    "Content-Type": "application/json",
}

response = requests.request("GET", url, json=payload, headers=headers)

print(response.text)
