import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")

if not BASE_URL or not API_KEY or not MODEL:
    raise ValueError("Missing configuration in .env file.")

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

stream = client.chat.completions.create(
    model = os.getenv("MODEL"),
    messages = [
        {
            "role": "user",
            "content": "What is the AI"
        }
    ],
    stream=True
)

full_response = ""



for chunk in stream:
    if not chunk.choices:
        continue
    
    piece = chunk.choices[0].delta.content
    if piece:
        print(piece, end="", flush=True) # streaming output to console
        full_response += piece

print("\n\nFull response:", full_response) # i will send this to LLM for history
