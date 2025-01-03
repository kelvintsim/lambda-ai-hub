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


def get_id(photo: str, rowId: str) -> str:
    gen_n8n_url = Config.AVATAR_N8N_ENDPOINT
    data = {
        "prompt": f"{photo} Generate a cartoon style avatar to replace only the face of the person, please keep the original background, try to make the cartoon avatar as much alike to the person.",
        "rowId": rowId
    }
    response = requests.post(gen_n8n_url, auth=(account, password), json=data)
    task = response.json()
    task_id = task["taskId"]
    return task_id


def genphoto_handler(event: EventDict, context) -> dict[str, str]:
    prompt = event["body"]["prompt"]
    rowId = event["body"]["rowId"]
    task_id = get_id(prompt, rowId)
    return {"task_id": task_id}
