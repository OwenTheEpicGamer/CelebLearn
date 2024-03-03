import os
import dropbox
import dropbox.files
import requests
import dotenv

dotenv.load_dotenv(".env")

dbx = dropbox.Dropbox(os.environ["DROPBOX_KEY"])


def upload_all_local_files(character):
    for file in os.listdir("./videoaudio"):
        with open(os.path.join("./videoaudio", file), "rb") as f:
            if f.name.endswith(".mp4") and f.name.__contains__(character):
                data = f.read()
                dbx.files_upload(data, f"/obama.mp4")
            elif f.name.endswith(".mp3"):
                data = f.read()
                dbx.files_upload(data, f"/audio.mp3")
            else:
                continue

upload_all_local_files("walter")


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
    "path": "/obama.mp4",
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
new_link = "https://dl.dropboxusercontent.com" + after_com
print(new_link)


