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
gen_n8n_url = Config.AVATAR_N8N_ENDPOINT
get_n8n_url = Config.GET_N8N_ENDPOINT


def get_id(photo: str) -> str:
    response = requests.post(gen_n8n_url, auth=(account, password), json={"prompt": f"{photo} Generate a cartoon style avatar "})
    task = response.json()
    task_id = task["taskId"]
    return task_id

def get_photo(taskId: str) -> dict[str, str]:
    get_photo_url = urljoin(get_n8n_url, taskId)
    image = requests.get(get_photo_url, auth=(account, password), json={})
    image_id = image.json()
    return image_id

def genphoto_handler(event: EventDict, context) -> dict[str, str]:
    prompt = event["body"]["prompt"]
    task_id = get_id(prompt)
    return task_id

def getphoto_handler(event: EventDict, context) -> dict[str, str]:
    image = event["body"]["taskId"]
    image_id = get_photo(image)
    return image_id