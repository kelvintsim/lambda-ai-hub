import os


class Config:
    AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
    AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
    AZURE_VISION_KEY = os.environ.get("AZURE_VISION_KEY")
    AZURE_VISION_ENDPOINT = os.environ.get("AZURE_VISION_ENDPOINT")
