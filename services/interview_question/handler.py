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
    
    sample_user_prompt_1 = (
         "You are now a human resources manager, please generate 10 interview questions based on the applied role of the candidate: \n"
         "DevOps Engineer"
    )
    
    sample_response_1 = (
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

    sample_user_prompt_2 = (
         "You are now a human resources manager, please generate 10 interview questions based on the applied role of the candidate: \n"
         "Customer service officer"
    )

    sample_response_2 = (
        """
        {
        "1": "Can you describe your previous experience in customer service roles and how it has prepared you for this position?",
        "2": "How do you handle difficult or irate customers? Can you provide an example of a challenging customer interaction and how you resolved it?",
        "3": "Effective communication is crucial in customer service. How do you ensure clear and concise communication with customers, both verbally and in writing?",
        "4": "In a fast-paced customer service environment, how do you prioritize and manage multiple customer inquiries or issues simultaneously?",
        "5": "Problem-solving skills are essential in customer service. Can you share an example of a complex customer issue you resolved, and the steps you took to reach a satisfactory outcome?",
        "6": "How do you handle customer complaints? Can you provide an example of a time when you successfully turned a dissatisfied customer into a loyal one?",
        "7": "Attention to detail is important in customer service to ensure accuracy and avoid errors. How do you ensure accuracy in your work, such as processing orders or updating customer information?",
        "8": "Technology plays a significant role in modern customer service. What customer service software or tools are you familiar with, and how have you utilized them in your previous roles?",
        "9": "Empathy is crucial in providing exceptional customer service. How do you demonstrate empathy towards customers, especially in challenging or emotional situations?",
        "10": "Continuous learning and improvement are important in customer service. How do you stay updated with industry trends and customer service best practices to enhance your skills?"
        }
        """
    )
    
    user_prompt = (
         "You are now a human resources manager, please generate 10 interview questions based on the applied role of the candidate: \n"
         f"{role}"
    )

    chatgpt_data = {
        "messages": [
            {"role": "user", "content": sample_user_prompt_1},
            {"role": "assistant", "content": sample_response_1},
            {"role": "user", "content": sample_user_prompt_2},
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
    interview_questions = chatgpt_message.strip('"')
    return interview_questions

def get_lambda_response(questions: str) -> dict[str, str]:
    return questions

def lambda_handler(event: EventDict, context) -> dict[str, str]:
    role = event["body"]["role"]
    questions = ask_questions(role)
    return get_lambda_response(questions)
