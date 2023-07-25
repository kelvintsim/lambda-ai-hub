import asyncio
import os

import dotenv
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import AzureChatOpenAI

dotenv.load_dotenv()

llm = AzureChatOpenAI(
    deployment_name=os.getenv("DEPLOYMENT_NAME")
)

VERBOSE = True


def get_intent(message):
    intent_template = """Base on the following message and classify the user intent belongs to which on the those list below.
    Output the intent list with the highest probability. Only output the intent name no other text is allowed.
    
    User message: {message}
    
    Intent list:
    
    Informational intent: Users seeking information, answers, or explanations about a specific topic or question. Example search query: "What is the capital of France?"
    
    Navigational intent: Users looking for a specific website or online resource. Example search query: "Facebook login page"
    
    Transactional intent: Users intending to make a purchase or engage in a specific transaction. Example search query: "Buy iPhone 12 online"
    
    Commercial intent: Users researching products or services with the intention of making a purchase in the near future. Example search query: "Best laptops for gaming"
    
    Local intent: Users looking for information or services in a specific geographic location. Example search query: "Restaurants near me"
    
    Investigative intent: Users conducting in-depth research or analysis on a particular topic. Example search query: "Causes and effects of climate change"
    
    Social intent: Users seeking to connect with others, engage in social media activities, or find social recommendations. Example search query: "Best workout groups on Facebook
    
    Output:"""""

    prompt = PromptTemplate(
        template=intent_template,
        input_variables=['message'])

    chain = LLMChain(llm=llm, prompt=prompt, verbose=VERBOSE)

    return chain.run(message=message)


def few_shot_generation(message, generation_prompt, evaluation_prompt, count=3, return_count=1):
    tasks = []

    gen_chain = LLMChain(llm=llm, prompt=generation_prompt, verbose=VERBOSE)

    for i in range(count):
        tasks.append(gen_chain.run(message=message))

    eval_chain = LLMChain(llm=llm, prompt=evaluation_prompt, verbose=VERBOSE)

    eval_tasks = []

    for idx, option in enumerate(tasks):
        eval_tasks.append((option, eval_chain.run(message=message, option=option)))

    return sorted(eval_tasks, key=lambda x: x[1], reverse=True)[:return_count]


intent = get_intent("How to create a go kart for kids at home")
strategy_gen_template = "You try to suggest a general strategy to solve this kind {message} reqeust? List it down step by step. Just output the steps. Output:"
strategy_gen_prompt = PromptTemplate(template=strategy_gen_template, input_variables=['message'])
strategy_eval_template = "You are going to rate the following strategy that aim to solve the {message} request. The scale from 0 to 100. 0 means the strategy is totally wrong. 100 means the strategy is totally correct. Only return the numeric value no other text is allowed.\n\nStrategy:{option}\n\nOutput:"
strategy_eval_prompt = PromptTemplate(template=strategy_eval_template, input_variables=['message', 'option'])
best_strategy = few_shot_generation(message=intent,
                                    generation_prompt=strategy_gen_prompt,
                                    evaluation_prompt=strategy_eval_prompt)

print(intent, best_strategy)

example_gen_template = f"Base on the following steps. Can you create an example that strictly follow the suggested steps to solve a {intent} request. Suggested Steps:{{message}} Output:"
example_gen_prompt = PromptTemplate(template=example_gen_template, input_variables=['message'])
example_eval_template = f"You are going to rate the following example that intent to help a AI agent to solve {intent} request. The scale from 0 to 100. 0 means the strategy is totally wrong. 100 means the example is totally fit for solve the reqeust. Only return the numeric value no other text is allowed.\n\nExample:{{option}}\n\nOutput:"
example_eval_prompt = PromptTemplate(template=example_eval_template, input_variables=['option'])
examples = few_shot_generation(message=intent,
                               generation_prompt=example_gen_prompt,
                               evaluation_prompt=example_eval_prompt,
                               count=10,
                               return_count=3)

print(examples)
