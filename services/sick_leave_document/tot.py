import os

from langchain import PromptTemplate, LLMChain
from langchain.chat_models import AzureChatOpenAI

# import dotenv

# dotenv.load_dotenv()

llm = AzureChatOpenAI(
    deployment_name=os.getenv("DEPLOYMENT_NAME")
)

step = 3

states = 5

# Creative writing task
zero_shot_prompt_template = f"""You are going to create a article for the following topic.
First you need to develop a {step} steps plan for create the articles 
{{topic}}"""

zero_shot_prompt = PromptTemplate(
    template=zero_shot_prompt_template,
    input_variables=['topic']
)

zero_shot_chain = LLMChain(llm=llm, prompt=zero_shot_prompt)

level_1_states = []

for i in range(states):
    result = zero_shot_chain.run(topic="How to learn english.")
    level_1_states.append(result)

print("result: ", level_1_states)

votes = ['3', '3', '3', '3', '3']
v_count = {}
for v in votes:
    v_count[v] = v_count.get(v, 0) + 1

# find the most voted result
max_voted = max(v_count, key=v_count.get)
