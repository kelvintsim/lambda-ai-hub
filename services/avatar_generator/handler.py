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

def get_id(photo: str) -> str:
    gen_n8n_url = Config.AVATAR_N8N_ENDPOINT
    response = requests.post(gen_n8n_url, auth=(account, password), json={"prompt": f"{photo} Generate a cartoon style avatar for the person, try to keep the appearance as similar as possible"})
    task = response.json()
    task_id = task["taskId"]
    return task_id

def genphoto_handler(event: EventDict, context) -> dict[str, str]:
    prompt = event["body"]["prompt"]
    task_id = get_id(prompt)
    return task_id