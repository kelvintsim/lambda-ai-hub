from langchain import PromptTemplate

from intents.information_intent import examples
import os

import dotenv
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import AzureChatOpenAI

dotenv.load_dotenv()

llm = AzureChatOpenAI(
    deployment_name=os.getenv("DEPLOYMENT_NAME")
)

VERBOSE = True

template = f"""You are a helpful AI assistance.

{examples}

Let try to help the human to solve the "{{request}}" request. Lets do it step by step

Output:"""

prompt = PromptTemplate(template=template, input_variables=['request'])

chain = LLMChain(llm=llm, prompt=prompt, verbose=VERBOSE)

print(chain.run(request="What is the best beaches in the world?"))
