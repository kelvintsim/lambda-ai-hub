import time
from typing import List, Tuple

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


def url_is_word_document(url):
    return url.endswith(".doc") or url.endswith(".docx")


def convert_word_document_to_pdf(image_url):
    print('converting word document to pdf')
    url = "https://u5b66nfy0j.execute-api.ap-east-1.amazonaws.com/dev/from_url"
    response = requests.post(url, {"url": image_url})

    print(response.json())

    return response.json()["url"]


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
        Payload=json.dumps(cv_info)
    )
    return cv_info


def get_questions_id_from_components(component_name_list: Tuple, components) -> List[str]:
    result = []

    for name in component_name_list:
        for c in components:
            if name in c["name"]:
                result.append(c["id"])
                break
    return result


def questions(event, context):
    url = event["image"]
    print(url)

    role = event["role"]
    print(role)

    record_id = event["record_id"]
    print(record_id)

    worksheet_id = os.getenv("WORKSHEET_ID")
    print(worksheet_id)

    if url_is_word_document(url):
        url = convert_word_document_to_pdf(url)

    cv_data = get_document_data(get_azure_ocr_data(url))

    cv_experience = json.loads(cv_data)

    experience = cv_experience["workExperience"]

    education = cv_experience["Education"]

    ability = cv_summarizer(experience, education)
    print(ability)

    response = get_questions(ability, role)

    questions = json.loads(response)

    test = requests.get(f"https://api.lancode.com/worksheet/api/v1/open/worksheets/{worksheet_id}", headers=headers)

    fields = get_questions_id_from_components(('Question 1',
                                               'Question 2',
                                               'Question 3',
                                               'Question 4',
                                               'Question 5',
                                               'Question 6',
                                               'Question 7',
                                               'Question 8',
                                               'Question 9',
                                               'Question 10'),
                                              test.json()["data"]["components"])

    print("question ids: ", fields)
    print("questions: ", questions.values())

    questions_list = zip(fields, questions.values())

    value = {"fields": dict(questions_list)}

    code = requests.put(f"https://api.lancode.com/worksheet/api/v1/open/worksheets/{worksheet_id}/records/{record_id}",
                        headers=headers, data=json.dumps(value))

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
        Payload=json.dumps(cv_info)
    )
    return cv_info


def parse(event, context):
    url = event["image"]
    print(url)

    record_id = event["record_id"]
    print(record_id)

    worksheet_id = os.getenv("WORKSHEET_ID")
    print(worksheet_id)

    if url_is_word_document(url):
        url = convert_word_document_to_pdf(url)

    azure_ocr_data = get_azure_ocr_data(url)

    get_llm_tries = 0
    get_llm_limit = 3
    time.sleep(1)

    cv_content = None

    while get_llm_tries < get_llm_limit:
        try:

            cv_data = get_document_data(azure_ocr_data)

            print("cv_data: ", cv_data)

            cv_content = json.loads(cv_data)
            break

        except Exception as e:
            print("get llm error: ", e)
            get_llm_tries += 1
            time.sleep(0.5)
            continue

    test = requests.get(f"https://api.lancode.com/worksheet/api/v1/open/worksheets/{worksheet_id}", headers=headers)

    # result = list(value["id"] for value in test.json()["data"]["components"])

    # cv_fields = result[1:-6]

    cv_field_names = ('name',
                      'mobile',
                      'email',
                      'sex',
                      'workExperience',
                      'lastCompanyName',
                      'Education',
                      'applied_role')

    cv_fields = get_questions_id_from_components(cv_field_names,
                                                 test.json()["data"]["components"])

    cv_info = zip(cv_fields, cv_content.values())

    fields = dict(cv_info)

    raw_data_column_id = get_questions_id_from_components(("raw data",),
                                                          test.json()["data"]["components"])

    fields[raw_data_column_id[0]] = cv_data

    value = {"fields": fields}

    code = requests.put(f"https://api.lancode.com/worksheet/api/v1/open/worksheets/{worksheet_id}/records/{record_id}",
                        headers=headers, data=json.dumps(value))

    print(code.json())

    # raw_data_fields = result[-6]
    #
    # print(raw_data_fields)
    #
    # raw_data = {raw_data_fields: cv_data}
    #
    # raw_data_field = {"fields": raw_data}
    #
    # print(raw_data)
    #
    # raw = requests.put(f"https://api.lancode.com/worksheet/api/v1/open/worksheets/{worksheet_id}/records/{record_id}",
    #                    headers=headers, data=json.dumps(raw_data_field))
    #
    # print(raw.json())

    return (code.json())

# class Event:
#     def __init__(self, img_path):
#         self.img_path = img_path

#     def get(self, key):
#         return getattr(self, key)


# result = parse(Event(
#     img_path='./examples/img1.jpg'),
#     None)

# print(result)
