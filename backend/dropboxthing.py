import os
import dropbox
import dropbox.files
import requests

with open("backend/TOKEN.txt", "r") as f:
    TOKEN = f.read()

dbx = dropbox.Dropbox(TOKEN)


def upload_all_local_files():
    for file in os.listdir("backend/videoaudio"):
        with open(os.path.join("backend/videoaudio", file), "rb") as f:
            data = f.read()
            dbx.files_upload(data, f"/{file}")


upload_all_local_files()

access_token = TOKEN

url = "https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

data = {
    "path": "/audio.wav",
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
after_com = url[index_of_com + len(".com") :]
new_link = "https://dl.dropboxusercontent.com" + after_com
print(new_link)


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
after_com = url[index_of_com + len(".com") :]
new_link = "https://dl.dropboxusercontent.com" + after_com
print(new_link)
