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
gen_n8n_url = Config.GET_N8N_ENDPOINT

def genphoto_handler(event: EventDict, context) -> dict[str, str]:
    print(event)
    prompt = event["body"]["prompt"]
    record = event["body"]["rowId"]
    gen_photo_url = urljoin(gen_n8n_url, prompt)
    response = requests.post(gen_photo_url, auth=(account, password), json={"rowId": record})
    print(response.json())
    return response.json()