
import json
from datetime import datetime
import requests


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate_sum(a: float, b: float):
    return a + b


def get_city_weather(city: str):
    url = f"https://wttr.in/{requests.utils.quote(city)}?format=3"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text.strip()


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get current date and time",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_sum",
            "description": "Add two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_city_weather",
            "description": "Get city weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                },
                "required": ["city"],
            },
        },
    },
]


FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time": get_current_time,
    "calculate_sum": calculate_sum,
    "get_city_weather": get_city_weather,
}


def run_tool(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments or "{}")

    print(f"[TOOL] {name} | Args: {args}")

    fn = FUNCTION_NAME_TO_FUNCTION_MAP.get(name)

    if fn is None:
        return f"Unknown tool: {name}"

    try:
        result = fn(**args)
        print(f"[RESULT] {result}")
        return result
    except Exception as e:
        print(f"[ERROR] {e}")
        return str(e)
