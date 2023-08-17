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
    record_id = event["body"]["record_id"]
    cv_info = {
            "image": image,
            "role": role,
            "record_id": record_id
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
    
    record_id = event["record_id"]
    print(record_id)
    
    worksheet_id = os.getenv("WORKSHEET_ID")
    print(worksheet_id)
    
    cv_data = get_document_data(get_azure_ocr_data(url))
    
    cv_experience = json.loads(cv_data)

    experience = cv_experience["workExperience"] 
    
    education = cv_experience["Education"]
    
    ability = cv_summarizer(experience, education)
    print(ability)
    
    response = get_questions(ability, role)
    
    questions = json.loads(response)
    
    test = requests.get(f"https://api.lancode.com/worksheet/api/v1/open/worksheets/{worksheet_id}", headers = headers)
    
    print(test.json())
    
    result = list(value["id"] for value in test.json()["data"]["components"])
    
    fields = result[2:-5]
    
    questions_list = zip(fields, questions.values())
    
    value = {"fields": dict(questions_list)}

    code = requests.put(f"https://api.lancode.com/worksheet/api/v1/open/worksheets/{worksheet_id}/records/{record_id}", headers = headers, data = json.dumps(value))
    
    print(code.json())
    
    return code.json()

def trigger_ocr(event, context):
    print(event)
    image = event["body"]["img_path"]
    record_id = event["body"]["record_id"]
    cv_info = {
            "image": image,
            "record_id": record_id
        }
    lambda_client.invoke(
        FunctionName=os.getenv("FUNCTION_NAME"),
        InvocationType='Event',
        Payload= json.dumps(cv_info)
    )
    return cv_info

def parse(event, context):
    url = event["image"]
    print(url)
    
    record_id = event["record_id"]
    print(record_id)
    
    worksheet_id = os.getenv("OCR_WORKSHEET_ID")
    print(worksheet_id)
    
    cv_data = get_document_data(get_azure_ocr_data(url))
    
    cv_content = json.loads(cv_data)
    
    test = requests.get(f"https://api.lancode.com/worksheet/api/v1/open/worksheets/{worksheet_id}", headers = headers)
    
    print(test.json())
    
    result = list(value["id"] for value in test.json()["data"]["components"])
    
    fields = result[1:-5]
    
    cv_info = zip(fields, cv_content.values())
    
    value = {"fields": dict(cv_info)}

    code = requests.put(f"https://api.lancode.com/worksheet/api/v1/open/worksheets/{worksheet_id}/records/{record_id}", headers = headers, data = json.dumps(value))
    
    print(code.json())


# class Event:
#     def __init__(self, img_path):
#         self.img_path = img_path

#     def get(self, key):
#         return getattr(self, key)


# result = parse(Event(
#     img_path='./examples/img1.jpg'),
#     None)

# print(result)
