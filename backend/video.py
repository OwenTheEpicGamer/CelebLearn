import requests

url = "https://api.synclabs.so/video"

payload = {
    "audioUrl": "https://dl.dropboxusercontent.com/scl/fi/ss9083rbmf611kinknmui/out-copy.wav?rlkey=7o89ees8g66e83fgrguol6i8c&dl=0",
    "maxCredits": 5000,
    "model": "wav2lip++",
    "synergize": True,
    "videoUrl": "https://dl.dropboxusercontent.com/scl/fi/r71sl46ii99v6g6wn6qdc/obama.mp4?rlkey=d1elxcxk0eak9wbkz8du4z7cq&dl=0",
    "webhookUrl": "https://discord.com/api/webhooks/1213669655202234418/To6ZT8XiqiLas5t1_vx5TrjIxQJS6KAwzNPYNCQmIG1RdhRVLQ056boiWJeiIXExrC10"
}
headers = {
    "x-api-key": "4e2ba9af-22ca-4c5b-9c0d-8061f3fe4213",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)


import requests

# url = f"https://api.synclabs.so/video/{response.json()['id']}
url = f"https://api.synclabs.so/video/8b206f92-5dc9-4240-bd8f-831f0b7b8a4e"

headers = {
    "x-api-key": "4e2ba9af-22ca-4c5b-9c0d-8061f3fe4213",
    "Content-Type": "application/json"
}

response = requests.request("GET", url, headers=headers)

print(response.text)

