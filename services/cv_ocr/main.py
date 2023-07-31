from services import get_document_data, get_questions, get_azure_ocr_data, cv_summarizer
import json 

def get_experience(event, context):
    
    url = event["body"]["img_path"]
    
    cv_data = get_document_data(get_azure_ocr_data(url))
    
    cv_experience = json.loads(cv_data)
    
    print(cv_experience)
    
    experience = cv_experience["job_experiences"] 
    
    education = cv_experience["educations"]
    
    ability = cv_summarizer(experience, education)
    
    print(ability)
    
    return ability
    
def questions(event, context):
    
    role = event["body"]["role"]
    
    ability = event["body"]["ability"]
    
    response = get_questions(ability, role)
    
    print(ability)
    
    print(response)
    
    return response

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
