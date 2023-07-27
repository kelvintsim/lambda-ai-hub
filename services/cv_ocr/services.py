import os
# import dotenv

import requests
import validators
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from dataclasses import dataclass
import json

from langchain.schema import HumanMessage
from langchain.tools import format_tool_to_openai_function

# dotenv.load_dotenv()


def get_azure_ocr_data(img_path):
    config = AzureOcrConfig(
        endpoint=os.getenv("AZURE_VISION_ENDPOINT"),
        api_key=os.getenv("AZURE_VISION_KEY")
    )
    if not validators.url(img_path):
        engine = AzureOcr(config=config)
    else:
        engine = AzureUrlOcr(config=config)

    result = engine.ocr(img_path)['readResult']['content']

    return result


def get_document_data(txt: str):
    template = """Base on the following information, try you best to guess the information in the resume.
    The following information in table structure. The last column is the text and first 4 columns are the corresponding 
    location of the text on the document.
    Output the candidate name, applied role, phone number, gender, job experiences, educations, age.
    You have to strictly follow the output format.

    Output example :
    '{{ 
    "candidate name": "Patrick Star",
    "applied role": "Senior software engineer",
    "phone number": "6777 8888",
    "gender": "male",
    "job experiences": "Senior Software Engineer, Microsoft, Los Angeles, CA August 2019-Current
    Manage a software engineering team of 15+ personnel to build innovative web applications using Agile-Waterfall methodologies, oversee all aspects of full-stack development, and identify opportunities to enhance the user experience
    Identify creative solutions and workflow optimizations to improve deployment timelines and reduce project roadblocks during development lifecycles
    Serve as the Microsoft Azure SME for the software engineering department and resolve escalated sodftware issues from junior team members",
    "educations": "Hong Kong University",
    "age": "25",
    }}'

    Information:
    {txt}

    Output:
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=['txt']
    )

    llm = AzureChatOpenAI(
        deployment_name=os.getenv("DEPLOYMENT_NAME")
    )

    chain = LLMChain(llm=llm,
                     prompt=prompt)

    return chain.run(txt=txt)


def get_score(application: dict, document_data: str):
    template = """You need to verify 2 sets of data and give grade them. The grade is A, B and C. 
    A means you are very confident that the document data is enough to support the leave applicatoin. 
    B means are you not sure the document data is enough or not.
    C means are you sure the document data is not enough to support the leave application.
    
    First set of data is the sick leave application data. The second set of data is information from the application supporting document. 
    If the subject's name or applied date doesn't match then you should grade them C.
    If the document data "Invalid supporting document" return C with reason of invalid supporting document.
    
    Output Example 1:
    '{{
        "grade": "A",
        "reason": ""
    }}'
    === End of example 1
    
    Output Example 2:
    '{{
        "grade": "B",
        "reason": "No subject name in document data"
    }}'
    === End of example 2
    
    Output Example 3:
    '{{
        "grade": "C",
        "reason": "Date doesn't match"
    }}'
    === End of example 3
    
    Lets start!
    
    Application Data:
    {application_data}
    
    Document Data:
    {document_data}
    
    Output:
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=['application_data', 'document_data']
    )

    llm = AzureChatOpenAI(
        deployment_name=os.getenv("DEPLOYMENT_NAME")
    )

    chain = LLMChain(llm=llm,
                     prompt=prompt, )

    return chain.run(application_data=application, document_data=document_data)


@dataclass
class AzureOcrConfig:
    endpoint: str
    api_key: str


class AzureOcr:
    def __init__(self, config: AzureOcrConfig):
        self._config = config

    def ocr(self, image_path: str):
        url = self._get_url()
        headers = self._get_headers()
        data = self._get_data(image_path)
        response = requests.post(url, headers=headers, data=data)
        return response.json()

    def _get_url(self) -> str:
        endpoint = self._config.endpoint
        api_version = '2023-02-01-preview'
        language = 'en'
        path = f'computervision/imageanalysis:analyze?api-version={api_version}&features=read&language={language}'
        url = requests.compat.urljoin(endpoint, path)
        return url

    def _get_headers(self) -> dict:
        api_key = self._config.api_key
        headers = {
            'Ocp-Apim-Subscription-Key': api_key,
            'Content-Type': self._get_content_type()
        }
        return headers

    def _get_content_type(self) -> str:
        return 'application/octet-stream'

    def _get_data(self, image_path: str) -> bytes:
        with open(image_path, 'rb') as f:
            data = f.read()
        return data


class AzureUrlOcr(AzureOcr):
    def __init__(self, config: AzureOcrConfig):
        super().__init__(config)

    def _get_content_type(self) -> str:
        return 'application/json'

    def _get_data(self, image_url: str) -> str:
        data = {
            'url': image_url
        }
        return json.dumps(data)





