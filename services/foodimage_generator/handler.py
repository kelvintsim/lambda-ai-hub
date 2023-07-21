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
gen_n8n_url = Config.GENERATE_N8N_ENDPOINT
get_n8n_url = Config.GET_N8N_ENDPOINT

def get_id(prompt: str) -> str:
    gen_photo_url = urljoin(gen_n8n_url, prompt)
    task = requests.post(gen_photo_url, auth=(account, password), json={})
    task_id = task["taskId"]
    return task_id

def get_photo(taskId: str) -> dict[str, str]:
    get_photo_url = urljoin(get_n8n_url, taskId)
    image = requests.get(get_photo_url, auth=(account, password), json={})
    image_id = image.json()
    return image_id

def lambda_handler(event: EventDict, context) -> dict[str, str]:
    prompt = event["body"]["prompt"]
    task_id = get_id(prompt)
    image_id = get_photo(task_id)
    return image_id
