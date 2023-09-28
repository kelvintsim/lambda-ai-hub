from typing import TypedDict
import requests
import datetime
from requests.compat import urljoin
from config import Config

class EventDict(TypedDict):
    type: str
    name: str

account = Config.MIDJOURNEY_ACCOUNT
password = Config.MIDJOURNEY_PASSWORD
avatar_n8n_url = Config.AVATAR_N8N_ENDPOINT

# def get_id(photo: str) -> str:
#     gen_n8n_url = Config.AVATAR_N8N_ENDPOINT
#     response = requests.post(gen_n8n_url, auth=(account, password), json={"prompt": f"{photo} Generate a cartoon style avatar to replace only the face of the person, please keep the original background, try to make the cartoon avatar as much alike to the person."})
#     task = response.json()
#     task_id = task["taskId"]
#     return task_id

# def genphoto_handler(event: EventDict, context) -> dict[str, str]:
#     prompt = event["body"]["prompt"]
#     task_id = get_id(prompt)
#     return task_id

def genphoto_handler(event: EventDict, context) -> dict[str, str]:
    photo = event["body"]["photo"]
    record = event["body"]["rowId"]
    prompt = f"{photo} Generate a cartoon style avatar to replace only the face of the person, please keep the original background, try to make the cartoon avatar as much alike to the person."
    gen_photo_url = urljoin(avatar_n8n_url, prompt)
    response = requests.post(gen_photo_url, auth=(account, password), json={"prompt": f"{photo} Generate a cartoon style avatar to replace only the face of the person, please keep the original background, try to make the cartoon avatar as much alike to the person.", "rowId": record})
    print(response.json())
    return response.json()