import os
import asyncio

from langchain import PromptTemplate, LLMChain
from langchain.chat_models import AzureChatOpenAI


# import dotenv

# dotenv.load_dotenv()


llm = AzureChatOpenAI(
    deployment_name=os.getenv("DEPLOYMENT_NAME")
)

zero_shot_cot_prompt_template = """Q: A juggle can juggle 16 balls. Half of the balls are golf balls, and half of the golf are blue. How many blue golf balls are there?
A: Let's think step by step.

Q:{input}"""

zero_shot_cot_prompt = PromptTemplate(
    template=zero_shot_cot_prompt_template,
    input_variables=['input']
)

zero_shot_cot_chain = LLMChain(llm=llm, prompt=zero_shot_cot_prompt)

q_input = "Students studied the revolution of Earth around the Sun. During which month will Florida have the most sunlight energy available? (a)March.(b)June.(c) September. (d) December."

counter = 3


async def run(_input):
    return await zero_shot_cot_chain.arun(input=_input)


async def main(_input):
    result = []
    for i in range(counter):
        result.append(asyncio.create_task(run(_input)))

    await asyncio.wait(result)

    print("Result:", result)

    return result


output = asyncio.run(main(q_input))

text = "\n============\n\n".join(o.result() for o in output)

self_consistency_template = """3 other agents provide the answers for the following question. 
You need to analyze the answers especially on the reasoning on how the get the answers then return the best result.

Question:
{question}

Agent Answers:
{answers}

Output:"""

self_consistency_prompt = PromptTemplate(
    template=self_consistency_template,
    input_variables=['question', 'answers']
)

self_consistency_chain = LLMChain(llm=llm, prompt=self_consistency_prompt)

final_answer = self_consistency_chain.run(question=q_input, answers=text)

# Output:
print("Output:", output)
print("text:", text)
print("=" * 10 + "\n\n")
print('final_answer:', final_answer)
