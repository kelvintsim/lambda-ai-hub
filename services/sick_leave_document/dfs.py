import os

# import dotenv
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import AzureChatOpenAI

# dotenv.load_dotenv()

llm = AzureChatOpenAI(
    deployment_name=os.getenv("DEPLOYMENT_NAME")
)

base_template = """You are going to solve the following problem step by step.
Question: {question}

Give you best next step to solve the problem.

%previous_placeholder%

Output:"""

VERBOSE = False

path = []


def plan_generation(problem, template, previous=[]):
    if len(previous) == 0:
        template = template.replace("%previous_placeholder%", "")
    else:
        template = template.replace("%previous_placeholder%", "Previous Step:\n" + '\n'.join(previous))

    prompt = PromptTemplate(
        template=template,
        input_variables=['question'])

    chain = LLMChain(llm=llm, prompt=prompt, verbose=VERBOSE)

    return chain.run(question=problem)


def evaluate(problem, current, previous=None):
    eval_template = """Following are the proposed solution for the problem. You try to evaluate the solution and give a score for the solution.
    The scale from 0 to 100. 0 means the solution is totally wrong. 100 means the solution is totally correct. Only return the numeric value no other text is allowed.
    
    Problem:{problem}
    
    Steps:{steps}

    Output:"""

    prompt = PromptTemplate(
        template=eval_template,
        input_variables=['steps', 'problem'])

    chain = LLMChain(llm=llm, prompt=prompt, verbose=VERBOSE)

    steps = f"{previous}\n{current}" if previous is not None else current

    return chain.run(problem=problem,
                     steps=steps,
                     verbose=VERBOSE)


def satisfaction_check(question, proposal):
    eval_template = """Following is the proposed solution for the problem.
    If you think  you can follow the proposed solution and solve the problem, then return YES otherwise return NO. 
    Only return YES or NO.
    
    Question:
    {question}
    
    Solution:
    {solution}

    Output:"""

    prompt = PromptTemplate(
        template=eval_template,
        input_variables=['solution', 'question'])

    chain = LLMChain(llm=llm, prompt=prompt)

    return chain.run(solution=proposal, question=question, verbose=VERBOSE)


def expend(question, selection):
    temp = []
    for i in range(iteration):
        p = plan_generation(question, base_template, selection)
        print("Generated plan: ", p)

        score = int(evaluate(question, p, selection))
        print("Score: ", score)
        temp.append((p, score))

    temp.sort(key=lambda x: x[1])

    print(temp)
    for t in temp:
        stack.insert(0, t)


def pick_item():
    potential = stack.pop(0)
    if potential is None:
        raise Exception("No more item in stack.")

    if potential[1] < threshold:
        current_select.pop()
        return pick_item()
    return potential[0]


def update_selection():
    current_select.append(pick_item())


def join_step_string():
    return "\n".join([stage[0] for stage in path])


target = "How to create a go kart at home?"

iteration = 3
max_depth = 20

scale = 100

threshold = 50

stack = []

current_select = []

counter = 0

while counter < max_depth:
    expend(target, current_select)
    print("Stack: ", stack)
    update_selection()
    print("Current select: ", current_select)
    # if satisfaction_check(target, "\n".join(current_select)) == "YES":
    #     print("Found the solution.")
    #     print(current_select)
    #     break
    counter += 1
