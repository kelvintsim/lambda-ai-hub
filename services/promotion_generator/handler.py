from typing import TypedDict
import requests
import datetime
from requests.compat import urljoin
from config import Config


class EventDict(TypedDict):
    type: str
    name: str


def ask_name(current_date: str) -> str:
    chatgpt_path = f"openai/deployments/{Config.AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-05-15"
    endpoint = Config.AZURE_OPENAI_ENDPOINT
    chatgpt_url = urljoin(endpoint, chatgpt_path)
    chatgpt_headers = {
        "Content-Type": "application/json",
        "api-key": Config.AZURE_OPENAI_KEY
    }
    
    sample_user_prompt = (
        "You are now a marketing manager from a restaurant, base on the current date, you have to generate a upcoming promotional event name with start_date, end_date, start_time, end_time and days each week in traditional chinese for the restaurant, please try to decide a event that fit with any upcoming festival."
        f"""
        current_date: 18-12-2023
        """
    )
    
    sample_response_1 = (
        "start_date: 25-12-2023, end_date: 29-12-2023, start_time: 18:00, end_time: 20:00, days: Saturday, Sunday, event_name: 聖誕周末盛宴"
    )
    
    sample_response_2 = (
        "start_date: 13-08-2023, end_date: 17-08-2023, start_time: 13:00, end_time: 15:00, days: Monday, Tuesday, Thursday, Saturday, event_name: 盛夏狂歡美食節"
    )
    
    sample_response_3 = (
        "start_date: 22-8-2023, end_date: 09-09-2023, start_time: 11:00, end_time: 14:00, days: Saturday, Sunday, event_name: 中秋美食節"
    )    
    
    user_prompt = (
        "You are now a marketing manager from a restaurant, base on the current date, you have to generate a upcoming promotional event name with start_date, end_date, start_time, end_time and days each week in traditional chinese for the restaurant, please try to decide a event that fit with any upcoming festival."
        f"""
        current_date: {current_date}
        """
    )
    
    chatgpt_data = {
        "messages": [
            {"role": "user", "content": sample_user_prompt},
            {"role": "assistant", "content": sample_response_1},
            {"role": "user", "content": sample_user_prompt},
            {"role": "assistant", "content": sample_response_2},
            {"role": "user", "content": sample_user_prompt},
            {"role": "assistant", "content": sample_response_3},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": 800,
        "temperature": 0.7,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": None
    }
    chatgpt_response = requests.post(chatgpt_url, headers=chatgpt_headers, json=chatgpt_data)
    chatgpt_message = chatgpt_response.json()["choices"][0]["message"]["content"]
    event_name = chatgpt_message.strip('"')
    return event_name

def get_lambda_response(name: str) -> dict[str, str]:
    return name

def lambda_handler(event: EventDict, context) -> dict[str, str]:
    current_date = datetime.datetime.now()
    name = ask_name(current_date)
    return get_lambda_response(name)
