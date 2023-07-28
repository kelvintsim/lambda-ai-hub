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

    Output example 1 (All information provided):
    '{{ 
    "candidate_name": "Patrick Star",
    "applied_role": "Senior software engineer",
    "phone_number": "6777 8888",
    "gender": "male",
    "job_experiences": "Senior Software Engineer, Microsoft, Los Angeles, CA August 2019-Current Manage a software engineering team of 15+ personnel to build innovative web applications using Agile-Waterfall methodologies, oversee all aspects of full-stack development, and identify opportunities to enhance the user experience Identify creative solutions and workflow optimizations to improve deployment timelines and reduce project roadblocks during development lifecycles Serve as the Microsoft Azure SME for the software engineering department and resolve escalated sodftware issues from junior team members",
    "educations": "Hong Kong University",
    "age": "25",
    }}'

    Output example 2 (missing partial information):
    '{{ 
    "candidate_name": "Patrick Star",
    "applied_role": "Senior software engineer",
    "phone_number": "Not mentioned",
    "gender": "male",
    "job_experiences": "Senior Software Engineer, Microsoft, Los Angeles, CA August 2019-Current Manage a software engineering team of 15+ personnel to build innovative web applications using Agile-Waterfall methodologies, oversee all aspects of full-stack development, and identify opportunities to enhance the user experience. Identify creative solutions and workflow optimizations to improve deployment timelines and reduce project roadblocks during development lifecycles. Serve as the Microsoft Azure SME for the software engineering department and resolve escalated sodftware issues from junior team members",
    "educations": "Hong Kong University",
    "age": "Not mentioned",
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

def cv_summarizer(experience: str, education: str):
    template = """You are now a human resources manager assistant, based on the provided experience and education from the candidate, you
    have to summarize the work experience, working knowledge and skills of the applicant. Please try to provide a concise summary of the candidate,
    in order to help your manager to design a set of questions that could accurately examine the ability of the applicant.

    First set of data is the applicant's past job experience. The second set of data is education of the applicant.
    
    Output Example:
    "The applicant has valuable work experience as a Website Intern at Fragrance Unlimited, where they optimized website categories and content, collaborated with a local SEO agency to drive organic traffic, and localized content for the USA market. They also demonstrated proficiency in Google Tag Manager and Google Analytics for tag implementation. Additionally, the applicant exhibited a customer-centric approach in managing the merchandise portfolio. Education-wise, they are pursuing a Master's in Linguistics (expected completion in June 2020) with a 3.85 GPA and hold a Bachelor's degree in Cognitive Science from UCLA with a GPA of 3.9. Their practical skills in website optimization, collaboration, and localization, coupled with a strong academic background, make them a promising candidate. The interview questions should focus on assessing their expertise in SEO practices, content localization, and how their academic knowledge complements their work experience."
    === End of example 
       
    Lets start!
    
    Experience:
    {experience}
    
    Education:
    {education}
    
    Output:
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=['experience', 'education']
    )

    llm = AzureChatOpenAI(
        deployment_name=os.getenv("DEPLOYMENT_NAME")
    )

    chain = LLMChain(llm=llm,
                     prompt=prompt, )

    return chain.run(experience=experience, education=education)


def get_questions(ability: str, role: str):
    template = """You are now a human resources manager, based on the provided ability summary of the candidate from your assistant, you
    have to generate a set of interview questions that can evaluate if the applicant is suitable to the applied role. Please try
    to think about interview questions that related to the role and can examine the past experience of the candidate. 

    First set of data is the applicant's summary. The second set of data is the applied role of the candidate. 
    
    Output Example 1:
    '{{
        "1": "As a Principal Security Consultant, you must have dealt with various security weaknesses in different systems. How do you think this experience will benefit you in the role of a computer scientist, and how would you approach integrating security measures into software development processes?",
        "2": "In your current position, you've tested a wide range of applications and technologies for security vulnerabilities with high accuracy. How do you plan to leverage your expertise in security testing to ensure the robustness and resilience of computer programs you develop or work with?",
        "3": "As an AI-focused computer scientist, how have you utilized artificial intelligence and machine learning in your previous projects or security assessments to enhance the identification and mitigation of security risks?",
        "4": "Tell us about a particularly challenging security issue you encountered during your tenure as a Principal Security Consultant. How did you approach solving it, and what lessons did you learn from the experience that could be applied in computer science research or development?",
        "5": "Presenting information at conferences demonstrates strong communication and presentation skills. How would you apply these skills in collaborating with other computer scientists or interdisciplinary teams on research projects or software development initiatives?",
        "6": "Your Master's in Advanced Computer Science with a focus on Artificial Intelligence is an excellent background for this role. How do you envision integrating your AI knowledge into the design and development of innovative computer applications or algorithms?",
        "7": "In the realm of AI ethics, how do you approach ensuring the responsible use of AI in your projects or applications, particularly when it comes to data privacy and bias mitigation?",
        "8": "As a computer scientist, problem-solving skills are crucial. Can you share an example of a complex technical problem you encountered in your previous roles, how you tackled it, and what were the outcomes?",
        "9": "Collaboration and teamwork are often required in computer science research and development. Tell us about an experience where you worked closely with a team to achieve a common goal, and how you contributed to the success of the project.",
        "10": "Technology is continuously evolving, and keeping up with advancements is vital. How do you stay updated with the latest trends and breakthroughs in both computer science and AI, and how do you see this continuous learning benefiting your future projects?"
    }}'
    === End of example 1
       
    Lets start!
    
    Ability:
    {ability}
    
    applied role:
    {role}
    
    Output:
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=['ability', 'role']
    )

    llm = AzureChatOpenAI(
        deployment_name=os.getenv("DEPLOYMENT_NAME")
    )

    chain = LLMChain(llm=llm,
                     prompt=prompt, )

    return chain.run(ability=ability, role=role)


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





