
import os
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from openai import OpenAI

# local modules
from tools import TOOLS, run_tool
from Utilities.utilities import log

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")

MAX_STEPS = 5

if not BASE_URL or not API_KEY or not MODEL:
    raise ValueError("Missing configuration in .env file.")

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

messages = [
    {
        "role": "system",
        "content": "Be humble and keep final answers under 20 words."
    }
]

while True:
    try:
        user_input = input("\n👨 Vikas: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n🤖 Assistant: Goodbye, Vikas!")
        break

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("🤖 Assistant: Goodbye, Vikas!")
        break

    if not user_input:
        continue

    turn_start_idx = len(messages)

    messages.append({
        "role": "user",
        "content": user_input
    })

    completed = False

    for step in range(MAX_STEPS):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                stream = True
            )
        except Exception as e:
            log(f"API request failed: {e}", level="ERROR")
            del messages[turn_start_idx:]
            print("🤖 Assistant: API request failed.")
            completed = True
            break

        msg = response.choices[0].message

        if not msg.tool_calls:
            answer = msg.content or "No response generated."

            messages.append({
                "role": "assistant",
                "content": answer
            })

            print(f"🤖 Assistant: {answer}")
            completed = True
            break

        messages.append(msg.model_dump(exclude_none=True))

        log(
            f"Step {step + 1}: "
            f"{len(msg.tool_calls)} tool call(s)",
            level="STEP"
        )

        for tool_call in msg.tool_calls:
            result = run_tool(tool_call)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

    if not completed:
        answer = "Maximum tool-calling rounds reached."

        messages.append({
            "role": "assistant",
            "content": answer
        })

        log(answer, level="WARN")
        print(f"🤖 Assistant: {answer}")
