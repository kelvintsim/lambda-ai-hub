from typing import TypedDict
import requests
from requests.compat import urljoin
from config import Config


class EventDict(TypedDict):
    type: str
    name: str


def ask_name(start_date: str, end_date: str, start_time: str, end_time: str, days: str) -> str:
    chatgpt_path = f"openai/deployments/{Config.AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-05-15"
    endpoint = Config.AZURE_OPENAI_ENDPOINT
    chatgpt_url = urljoin(endpoint, chatgpt_path)
    chatgpt_headers = {
        "Content-Type": "application/json",
        "api-key": Config.AZURE_OPENAI_KEY
    }
    user_prompt = (
        "Generate a promotion 'traditional chinese' event name for a restaurant base on the following period of date range, time range and days: \n"
        f"""
        date_range: {start_date} - {end_date}
        time_range: {start_time} - {end_time}
        days: {days}
        """
    )
    sample_response = (
        "中華美食工作日盛宴"
        "尊享中式午茶時光"
        "黄金蝦仁周中宴"
        "節日美饌周日珍宴"
        "聖夜之星美食之旅"
    )

    chatgpt_data = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "user", "content": sample_response},
        ],
        "max_tokens": 800,
        "temperature": 0.2,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": None
    }
    chatgpt_response = requests.post(chatgpt_url, headers=chatgpt_headers, json=chatgpt_data)
    return chatgpt_response

def get_lambda_response(name: str) -> dict[str, str]:
    return {
        "promotion_name": name
    }
    

def lambda_handler(event: EventDict, context) -> dict[str, str]:
    type = event["type"]
    name = event["name"]
    prompt = ask_name(type, name)
    return get_lambda_response(prompt)
