import os


class Config:
    MIDJOURNEY_ACCOUNT = os.environ.get("MIDJOURNEY_ACCOUNT")
    MIDJOURNEY_PASSWORD = os.environ.get("MIDJOURNEY_PASSWORD")
    GENERATE_N8N_ENDPOINT = os.environ.get("GENERATE_N8N_ENDPOINT")
    GET_N8N_ENDPOINT = os.environ.get("GET_N8N_ENDPOINT")