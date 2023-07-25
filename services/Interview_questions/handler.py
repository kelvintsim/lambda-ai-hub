from typing import TypedDict
import requests
from requests.compat import urljoin
from config import Config


class EventDict(TypedDict):
    type: str
    name: str


def ask_questions(role: str) -> str:
    chatgpt_path = f"openai/deployments/{Config.AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-05-15"
    endpoint = Config.AZURE_OPENAI_ENDPOINT
    chatgpt_url = urljoin(endpoint, chatgpt_path)
    chatgpt_headers = {
        "Content-Type": "application/json",
        "api-key": Config.AZURE_OPENAI_KEY
    }
    
    sample_user_prompt = (
         "You are now a human resources manager, please generate 10 interview questions based on the applied role of the candidate: \n"
         "DevOps Engineer"
    )
    
    sample_response = (
        """
        {
        "1": "Can you explain the main principles of DevOps and how they contribute to the software development lifecycle?",
        "2": "How do you approach automating the deployment process to ensure consistency and reliability across different environments?",
        "3": "Tell us about a challenging technical issue you encountered during a deployment. How did you identify the root cause, and what steps did you take to resolve it?",
        "4": "Collaboration is a vital aspect of DevOps. Can you provide an example of a successful collaboration experience with developers or operations teams to achieve a common goal?",
        "5": "Continuous Integration (CI) and Continuous Deployment (CD) are essential in the DevOps workflow. How have you utilized CI/CD tools to streamline the development process in your previous projects?",
        "6": "Security is a critical concern in DevOps. How do you ensure the security of the software during the development and deployment stages?",
        "7": "Configuration management plays a significant role in managing infrastructure. Which configuration management tools are you familiar with, and how have you used them in your previous projects?",
        "8": "Can you share your experience with cloud platforms and how you leverage them to build scalable and resilient infrastructures?",
        "9": "In a fast-paced development environment, unforeseen issues may arise. How do you handle incidents, and what steps do you take to prevent similar incidents in the future?",
        "10": "Continuous learning is crucial in the ever-evolving field of DevOps. How do you stay updated with the latest technologies and best practices in the industry?"
        }
        """
    )
    
    user_prompt = (
         "You are now a human resources manager, please generate 10 interview questions based on the applied role of the candidate: \n"
         f"{role}"
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
    interview_questions = chatgpt_message.strip('"')
    return interview_questions

def get_lambda_response(questions: str) -> dict[str, str]:
    return questions

def lambda_handler(event: EventDict, context) -> dict[str, str]:
    role = event["body"]["role"]
    questions = ask_questions(role)
    return get_lambda_response(questions)
