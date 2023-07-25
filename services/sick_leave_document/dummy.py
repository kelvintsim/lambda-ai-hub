import os

# import dotenv
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import AzureChatOpenAI

# dotenv.load_dotenv()

llm = AzureChatOpenAI(
    deployment_name=os.getenv("DEPLOYMENT_NAME")
)

zero_shot_prompt_template = "{input}"

zero_shot_prompt = PromptTemplate(
    template=zero_shot_prompt_template,
    input_variables=['input']
)

ocr_result = """{
    "captionResult": {
        "text": "a woman holding a megaphone and a banner",
        "confidence": 0.3932569921016693
    },
    "objectsResult": {
        "values": [
            {
                "boundingBox": {
                    "x": 312,
                    "y": 196,
                    "w": 113,
                    "h": 126
                },
                "tags": [
                    {
                        "name": "mammal",
                        "confidence": 0.67
                    }
                ]
            }
        ]
    },
    "denseCaptionsResult": {
        "values": [
            {
                "text": "a woman holding a megaphone and a banner",
                "confidence": 0.3932569921016693,
                "boundingBox": {
                    "x": 0,
                    "y": 0,
                    "w": 566,
                    "h": 630
                }
            },
            {
                "text": "a cartoon of a woman with long hair",
                "confidence": 0.5284445881843567,
                "boundingBox": {
                    "x": 98,
                    "y": 64,
                    "w": 172,
                    "h": 135
                }
            }
        ]
    },
    "modelVersion": "2023-02-01-preview",
    "metadata": {
        "width": 566,
        "height": 630
    },
    "tagsResult": {
        "values": [
            {
                "name": "clipart",
                "confidence": 0.9463722705841064
            },
            {
                "name": "illustration",
                "confidence": 0.8641341924667358
            },
            {
                "name": "graphic design",
                "confidence": 0.8575276136398315
            },
            {
                "name": "graphics",
                "confidence": 0.857180655002594
            },
            {
                "name": "design",
                "confidence": 0.6055671572685242
            },
            {
                "name": "cartoon",
                "confidence": 0.5315120220184326
            }
        ]
    }
}"""

zero_shot_chain = LLMChain(llm=llm, prompt=zero_shot_prompt)

best_result = None
best_score = None

count = 3

for i in range(count):

    result = zero_shot_chain.run(input=f"""Create a summary of the following OCR JSON data for various illustrations to 
    streamline your design projects. Explain the key information and elements of each illustration and categorize them 
    based on their relevance and usability for future design tasks.
    
    Example Summary: 
    This image can be categorized as relevant and usable for design projects related to activism, protests, or public speaking. The text descriptions and object recognition can help in selecting appropriate images for such projects, while the tags can help in identifying similar images for future use.
    ====End of Example
    
    OCR JSON Data: {ocr_result}
    
    Output Summary:""")

    _score = zero_shot_chain.run(input=f"""You are senior illustrator. The following text is the summary of an illustration
     that create from a AI agent. You need to rate it from 1 to 10 (10 is the best). The higher the score, the summary 
    is more useful for searching and retrieving for future design projects. Only output the numeric score.
    
    Summary:
    {result}
    
    Output:""")

    score = int(_score)

    print(f"Score: {score}")
    print(f"Result: {result}")

    if best_result is None:
        best_result = result
        best_score = score
    else:
        if score > best_score:
            best_result = result
            best_score = score

# result = zero_shot_chain.run(input=f"""You are a good ChatGPT prompt engineer. You are going to help me to create a prompt.
# I have a set of OCR JSON data of different illustrations. I need to create summary base on these JSON data. The reason I
# for is summary is that in any future design project, I can easily find relevant and proper illustration for the task.
# Output Prompt:""")

print(result)
