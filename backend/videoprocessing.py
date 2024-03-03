import json
import requests
import time

data = {
    "method": "POST",
    "url": "https://api.synclabs.so/video",
    "headers": {
        "accept": "application/json",
        "x-api-key": "4e2ba9af-22ca-4c5b-9c0d-8061f3fe4213",
        "Content-Type": "application/json"
    },
    "body": {
        "audioUrl": "https://drive.google.com/file/d/1FvPblbdPc0_rXliiszsqd9iQHOQjcAQi/view?usp=sharing",
        "videoUrl": "https://drive.google.com/file/d/1VhEa81-XqYv5RDehvkwVVEAggLqLN0iP/view?usp=sharing",
        "synergize": True,
        "maxCredits": 5000,
        "webhookUrl": "https://example.com/webhook",
        "model": "wav2lip++"
    }
}

# Send the POST request
response = requests.post(data['url'], json=data['body'], headers=data['headers'])

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print("POST request was successful")
    # Print the response data
    print("Response:", response.json())
# elif response.status_code == 201:
#     # Loop until the request is no longer pending or a timeout is reached
#     while response.json().get("status") == "PENDING":
#         # Wait for a few seconds before making the next request
#         time.sleep(5)
#
#         # Send another request to check the status
#         response = requests.post(data['url'], json=data['body'], headers=data['headers'])
#
#     # Once the request is no longer pending, print the actual response
#     print("Actual Response:", response.json())
else:
    print("POST request failed with status code:", response.status_code)

    print(response.json())


import requests

url = f"https://api.synclabs.so/video/{response.json()['id']}"
# url = f"https://api.synclabs.so/video/e81feefe-7465-4f25-8b83-2d9ce2fbceae"


headers = {
        "accept": "application/json",
        "x-api-key": "4e2ba9af-22ca-4c5b-9c0d-8061f3fe4213",
        "Content-Type": "application/json"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)

