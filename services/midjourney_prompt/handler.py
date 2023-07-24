from typing import TypedDict
import requests
from requests.compat import urljoin
from config import Config


class EventDict(TypedDict):
    type: str
    name: str


def ask_prompt(type: str, name: str) -> str:
    chatgpt_path = f"openai/deployments/{Config.AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-05-15"
    endpoint = Config.AZURE_OPENAI_ENDPOINT
    chatgpt_url = urljoin(endpoint, chatgpt_path)
    chatgpt_headers = {
        "Content-Type": "application/json",
        "api-key": Config.AZURE_OPENAI_KEY
    }
    user_prompt = (
        "Generate a prompt for Midjourney for the following item to generate images of it, please do not contain the word 'hot' in your prompt: \n"
        f"{type}: {name}"
    )
    sample_user_prompt = (
         "Generate a prompt for Midjourney for the following item to generate images of it, please do not contain the word 'hot' in your prompt: \n"
         "Food: 乾炒牛河"
    )
    sample_response_1 = (
        "Create vibrant and appetizing images of the popular Chinese dish, 乾炒牛河 (Dry Fried Beef Hor Fun), "
        "a delicious stir-fried flat rice noodle dish with tender slices of beef, bean sprouts, scallions, "
        "and a savory sauce. Capture the dish in all its glory, showcasing the glossy noodles, "
        "perfectly seared beef, and the vibrant mix of colors from the fresh vegetables. "
        "The images should evoke the enticing aroma and mouthwatering flavors of this classic Cantonese delicacy."
    )
    
    sample_response_2 = (
        f"""
        Capture the essence of 飯糰(rice ball), a traditional Japanese dish that combines a variety of ingredients such as rice, 
        vegetables, and protein, all beautifully rolled in a circular shape. 
        Showcase the vibrant colors and textures of the dish, highlighting the freshness of the vegetables, 
        the succulence of the protein, and the fluffy grains of rice. 
        The images should convey the harmony and balance of flavors in this visually appealing and delicious meal.
        """
    )

    chatgpt_data = {
        "messages": [
            {"role": "user", "content": sample_user_prompt},
            {"role": "assistant", "content": sample_response_1},
            {"role": "user", "content": sample_user_prompt},
            {"role": "assistant", "content": sample_response_2},
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
    midjourney_prompt = chatgpt_message.strip('"')
    return midjourney_prompt

def get_lambda_response(prompt: str) -> dict[str, str]:
    return {
        "prompt": prompt
    }

def lambda_handler(event: EventDict, context) -> dict[str, str]:
    type = event["body"]["type"]
    name = event["body"]["name"]
    prompt = ask_prompt(type, name)
    return get_lambda_response(prompt)
