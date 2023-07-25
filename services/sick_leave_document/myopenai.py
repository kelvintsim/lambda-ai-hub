import os

from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI, AzureChatOpenAI
# import dotenv
from langchain.llms import AzureOpenAI

# dotenv.load_dotenv()

# chain = get_openapi_chain("https://www.klarna.com/us/shopping/public/openai/v0/api-docs/")
#
# print(chain.run("What are some options for a men's large blue button down shirt"))


llm = AzureChatOpenAI(
    deployment_name=os.getenv("DEPLOYMENT_NAME")
)

chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template("{input}"))

print(chain.run(input="testing"))
