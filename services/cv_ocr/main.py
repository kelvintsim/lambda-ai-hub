from services import get_document_data, get_questions, get_azure_ocr_data, cv_summarizer
from boto3 import client as boto3_client
import json 
import requests
import os 

lambda_client = boto3_client('lambda', region_name="ap-southeast-1")

headers = {
    "X-APP-KEY": os.getenv("X_APP_KEY"),
    "X-APP-SIGN": os.getenv("X_APP_SIGN"),
    "Content-Type": "application/json"
}

def trigger_get_questions(event, context):
    print(event)
    image = event["body"]["img_path"]
    role = event["body"]["role"]
    cv_info = {
            "image": image,
            "role": role
        }
    lambda_client.invoke(
        FunctionName=os.getenv("FUNCTION_NAME"),
        InvocationType='Event',
        Payload= json.dumps(cv_info)
    )
    return cv_info
    
def questions(event, context):
    
    url = event["image"]
    print(url)
        
    role = event["role"]
    print(role)
    
    cv_data = get_document_data(get_azure_ocr_data(url))
    
    cv_experience = json.loads(cv_data)

    experience = cv_experience["job_experiences"] 
    
    education = cv_experience["educations"]
    
    ability = cv_summarizer(experience, education)
    print(ability)
    
    response = get_questions(ability, role)
    
    questions = json.loads(response)
    
    cv_questions = event | questions
    
    test = requests.get("https://api.lancode.com/worksheet/api/v1/open/worksheets/64c245c31fba346dc58353c1", headers = headers)
    
    result = list(value["id"] for value in test.json()["data"]["components"])
    
    fields = result[:-5]
    
    questions_list = zip(fields, cv_questions.values())
    
    value = {"fields": dict(questions_list)}

    code = requests.post("https://api.lancode.com/worksheet/api/v1/open/worksheets/64c245c31fba346dc58353c1/records/", headers = headers, data = json.dumps(value))
    
    print(code.json())
    
    return code.json()

def parse(event, context):
    img_path = event["body"]["img_path"]
    
    cv_data = get_document_data(get_azure_ocr_data(img_path))
    
    print(cv_data)
    
    return cv_data


# class Event:
#     def __init__(self, img_path):
#         self.img_path = img_path

#     def get(self, key):
#         return getattr(self, key)


# result = parse(Event(
#     img_path='./examples/img1.jpg'),
#     None)

# print(result)
