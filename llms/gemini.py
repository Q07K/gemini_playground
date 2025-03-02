import os

import google.generativeai as genai
from google.auth.exceptions import DefaultCredentialsError


def get_model_list_legacy():
    return [
        "models/gemini-1.5-pro",
        "models/gemini-1.5-pro-001",
        "models/gemini-1.5-pro-002",
        "models/gemini-2.0-pro-exp",
        "models/gemini-2.0-flash-thinking-exp",
    ]


def get_model_list():
    return [
        model.name
        for model in genai.list_models()
        if "generateContent" in model.supported_generation_methods
    ]


def valid_api_key():
    try:
        genai.configure(api_key=os.getenv("api_key"))
        genai.list_models()
        return True
    except DefaultCredentialsError:
        return False


def generate(
    model_name: str,
    system_prompt: str,
    document: str,
    query: str,
):
    model = genai.GenerativeModel(
        model_name=model_name, system_instruction=system_prompt
    )
    agent = model.start_chat(
        history=[
            {"role": "user", "parts": [document]},
        ]
    )
    for chunk in agent.send_message(content=query, stream=True):
        if chunk.text:
            yield chunk.text
