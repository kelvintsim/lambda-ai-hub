from typing import TypedDict
import requests
from requests.compat import urljoin
from sample_json import sample_json
from config import Config

class EventDict(TypedDict):
    url: str

def ocr(url: str) -> str:
    # post the file to the Azure Computer Vision service
    # join url with the api endpoint
    endpoint = Config.AZURE_VISION_ENDPOINT
    ocr_path = "computervision/imageanalysis:analyze?api-version=2023-02-01-preview&features=denseCaptions,caption,objects,tags&language=en"
    ocr_url = urljoin(endpoint, ocr_path)
    ocr_headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": "6a94184fcec440b3b64f8f0f6524c05d"
    }
    ocr_data = {
        "url": url
    }

    ocr_response = requests.post(ocr_url, headers=ocr_headers, json=ocr_data)
    return ocr_response.text

def ask_description(json: str) -> str:
    chatgpt_path = f"openai/deployments/{Config.AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-05-15"
    endpoint = Config.AZURE_OPENAI_ENDPOINT
    chatgpt_url = urljoin(endpoint, chatgpt_path)
    chatgpt_headers = {
        "Content-Type": "application/json",
        "api-key": Config.AZURE_OPENAI_KEY
    }
    system_prompt = (
        "Here is the image caption generated from Azure AI service for an image. "
        "Tell the user about the image with natural language to help him visualise it. "
        "Please only use 5 words or phrases to describe the content, main theme or categories of the photos. "
        "Don't mention that it is from Azure AI service. '.\n\n"
    )
    sample_response_1 = (
        "Gorgeous women, Sunny day, Money, beach, Endless sea"
    )
    
    sample_response_2 = (
        "Coding with computer, frustrated engineer, messy desk, bright environment, desolate"
    )

    chatgpt_data = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": sample_json},
            {"role": "assistant", "content": sample_response_1},
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": sample_json},
            {"role": "assistant", "content": sample_response_2},
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json},
        ],
        "max_tokens": 800,
        "temperature": 0,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": None
    }
    chatgpt_response = requests.post(chatgpt_url, headers=chatgpt_headers, json=chatgpt_data)
    chatgpt_message = chatgpt_response.json()["choices"][0]["message"]["content"]
    description = chatgpt_message.strip('"')
    return description

def get_lambda_response(description: str) -> dict[str, str]:
    return {
        "description": description
    }

def lambda_handler(event: EventDict, context) -> dict[str, str]:
    url = event["body"]["url"]
    ocr_json = ocr(url)
    description = ask_description(ocr_json)
    return get_lambda_response(description)
    