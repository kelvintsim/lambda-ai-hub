from typing import TypedDict
import requests
from requests.compat import urljoin
from config import Config


class EventDict(TypedDict):
    type: str
    name: str


def ask_background(company_name: str) -> str:
    chatgpt_path = f"openai/deployments/{Config.AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-05-15"
    endpoint = Config.AZURE_OPENAI_ENDPOINT
    chatgpt_url = urljoin(endpoint, chatgpt_path)
    chatgpt_headers = {
        "Content-Type": "application/json",
        "api-key": Config.AZURE_OPENAI_KEY
    }
    
    sample_user_prompt = (
         "Generate a background description for the following company in traditional chinese within 30 words: \n"
         "優科互聯網科技有限公司"
    )
    
    sample_response = (
        "優科互聯網科技有限公司是一家領先的科技公司，專注於創新網絡技術和數字解決方案，為客戶提供卓越的數字體驗和高效的互聯網解決方案。"
    )
    
    user_prompt = (
        "Generate a background description for the following company in traditional chinese within 30 words: \n"
        f"{company_name}"
    )

    chatgpt_data = {
        "messages": [
            {"role": "user", "content": sample_user_prompt},
            {"role": "assistant", "content": sample_response},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": 800,
        "temperature": 0.2,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": None
    }
    chatgpt_response = requests.post(chatgpt_url, headers=chatgpt_headers, json=chatgpt_data)
    chatgpt_message = chatgpt_response.json()["choices"][0]["message"]["content"]
    company_description = chatgpt_message.strip('"')
    return company_description

def get_lambda_response(desciption: str) -> dict[str, str]:
    return {
        "description": desciption
    }

def lambda_handler(event: EventDict, context) -> dict[str, str]:
    food_item = event["body"]["company_name"]
    background = ask_background(food_item)
    return get_lambda_response(background)
