from services import get_document_data, get_score, get_azure_ocr_data


def score(event, context):
    img_path = event["body"]["img_path"]

    application = event["body"]["application"]

    txt = get_azure_ocr_data(img_path)

    document_data = get_document_data(txt)

    response = get_score(application, document_data)

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
