from services import get_document_data, get_questions, get_azure_ocr_data


def questions(event, context):
    role = event["body"]["role"]
    experience = event["body"]["experience"]
    education = event["body"]["education"]
    response = get_questions(experience, education, role)
    return response


def parse(event, context):
    img_path = event["body"]["img_path"]

    return get_document_data(get_azure_ocr_data(img_path))


# class Event:
#     def __init__(self, img_path):
#         self.img_path = img_path

#     def get(self, key):
#         return getattr(self, key)


# result = parse(Event(
#     img_path='./examples/img1.jpg'),
#     None)

# print(result)
