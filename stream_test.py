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
            "content": "What is the weather of pune?"
        }
    ],
    stream=True
)

full_response = ""

for chunk in stream:
    if not chunk.choices[0]:
        continue
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
        full_response += content

print("\n\nFull response:", full_response) # i will send this to LLM for history
