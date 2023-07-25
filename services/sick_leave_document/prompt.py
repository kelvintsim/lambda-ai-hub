import os
import asyncio

from langchain import PromptTemplate, LLMChain
from langchain.chat_models import AzureChatOpenAI
from langchain.model_laboratory import ModelLaboratory

# import dotenv

# dotenv.load_dotenv()

llm = AzureChatOpenAI(
    deployment_name=os.getenv("DEPLOYMENT_NAME")
)

zero_shot_prompt_template = "{input}"

zero_shot_prompt = PromptTemplate(
    template=zero_shot_prompt_template,
    input_variables=['input']
)

zero_shot_chain = LLMChain(llm=llm, prompt=zero_shot_prompt)

zero_shot_cot_prompt_template = """Q: A juggle can juggle 16 balls. Half of the balls are golf balls, and half of the golf are blue. How many blue golf balls are there?
A: Let's think step by step.

Q:{input}"""

zero_shot_cot_prompt = PromptTemplate(
    template=zero_shot_cot_prompt_template,
    input_variables=['input']
)

zero_shot_cot_chain = LLMChain(llm=llm, prompt=zero_shot_cot_prompt)

chains = [
    zero_shot_chain,
    zero_shot_cot_chain
]

q_input = "Mehak bought 96 toys priced equally for Rs. 12960. The amount of Rs. 1015 is still left with him. Find the cost of each toy and the amount he had."
model_lab = ModelLaboratory(chains)
model_lab.compare(q_input)

