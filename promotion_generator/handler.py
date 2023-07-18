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
        "Generate a 'traditional chinese' promotion event name within 10 words for a restaurant base on the following period of date range, time range and days: \n"
        f"""
        date_range: {start_date} - {end_date}
        time_range: {start_time} - {end_time}
        days: {days}
        """
    )
    
    sample_response = (
        "聖誕美食工作日盛宴"
    )
    
    chatgpt_data = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "system", "content": sample_response}
        ],
        "max_tokens": 800,
        "temperature": 0.2,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": None
    }
    chatgpt_response = requests.post(chatgpt_url, headers=chatgpt_headers, json=chatgpt_data)
    chatgpt_message = chatgpt_response.json()["choices"][0]["message"]["content"]
    event_name = chatgpt_message.strip('"')
    return event_name

def get_lambda_response(name: str) -> dict[str, str]:
    return {
        "promotion_name": name
    }
    

def lambda_handler(event: EventDict, context) -> dict[str, str]:
    start_date = event["body"]["start_date"]
    end_date = event["body"]["end_date"]
    start_time = event["body"]["start_time"]
    end_time = event["body"]["end_time"]
    days = event["body"]["days"]
    name = ask_name(start_date, end_date, start_time, end_time, days)
    return get_lambda_response(name)
