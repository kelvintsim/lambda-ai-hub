from typing import TypedDict
import requests
from requests.compat import urljoin
from config import Config


class EventDict(TypedDict):
    type: str
    name: str


def ask_description(item: str) -> str:
    chatgpt_path = f"openai/deployments/{Config.AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-05-15"
    endpoint = Config.AZURE_OPENAI_ENDPOINT
    chatgpt_url = urljoin(endpoint, chatgpt_path)
    chatgpt_headers = {
        "Content-Type": "application/json",
        "api-key": Config.AZURE_OPENAI_KEY
    }
    
    sample_user_prompt = (
         "Generate a description for the following food item in traditional chinese within 30 words: \n"
         "乾炒牛河"
    )
    
    sample_response = (
        "乾炒牛河是一道香港特色的經典美食，也是廣受喜愛的中式炒麵類菜品之一。這道菜市以其豐富的口味和獨特的質感而聞名。"
        "乾炒牛河主要由絲狀的米粉和嫩滑的牛肉組成，通常伴隨著新鮮的蔬菜和香濃的醬汁。烹調過程中，"
        "廚師們巧妙地將牛肉、蔬菜和米粉一同爆炒，使其充分融合，每一口都能品嚐到美味的滋味。牛肉通常切成薄片，鮮嫩多汁，讓人食指大動。"
    )
    
    user_prompt = (
        "Generate a description for the following food item in traditional chinese within 30 words: \n"
        f"{item}"
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
    food_description = chatgpt_message.strip('"')
    return food_description

def get_lambda_response(desciption: str) -> dict[str, str]:
    return {
        "description": desciption
    }

def lambda_handler(event: EventDict, context) -> dict[str, str]:
    food_item = event["body"]["item"]
    description = ask_description(food_item)
    return get_lambda_response(description)
