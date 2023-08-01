from services import get_document_data, get_questions, get_azure_ocr_data, cv_summarizer
from boto3 import client as boto3_client
import json 
import requests

lambda_client = boto3_client('lambda', region_name="ap-southeast-1",)

def trigger_get_questions(event, context):
    image = event["body"]["img_path"]
    role = event["body"]["role"]
    cv_info = {
            "image": image,
            "role": role
        }
    lambda_client.invoke(
        FunctionName="cv-ocr-dev-cv_question",
        InvocationType='Event',
        Payload= json.dumps(cv_info)
    )
    
def get_questions(event, context):
    print(event)
    
    url = event["image"]
    print(url)
    
    role = event["role"]
    print(role)    
    
    cv_data = get_document_data(get_azure_ocr_data(url))
    
    cv_experience = json.loads(cv_data)

    experience = cv_experience["job_experiences"] 
    
    education = cv_experience["educations"]
    
    ability = cv_summarizer(experience, education)
    
    # response = get_questions(ability, role)
    
    print(ability)
    
    # print(response)
    
    # requests.post("https://www.lancode.com/workflow/api/v1/public/webhooks/NjRjOGNjNWZmMzFjZjIwNWRjNTU1ZTU2", json = {})
    
    return ability

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
