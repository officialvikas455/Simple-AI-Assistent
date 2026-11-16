
import json
from datetime import datetime
import requests

from Utilities.utilities import log
from rag import search

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate_sum(a: float, b: float):
    return a + b


def get_city_weather(city: str):
    url = f"https://wttr.in/{requests.utils.quote(city)}?format=3"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text.strip()

def search_and_summarize(
    query: str,
    max_results: int = 5,
    focus: str = "general"
) -> dict:
    """
    Search the web and summarize useful information.

    Args:
        query: Topic to research.
        max_results: Number of results (1-10).
        focus: general, technical, latest, or beginner.

    Returns:
        Search results and a structured summary.
    """
    if not query or not query.strip():
        raise ValueError("Query must be a non-empty string.")

    if not 1 <= max_results <= 10:
        raise ValueError("max_results must be between 1 and 10.")

    return {
        "query": query,
        "max_results": max_results,
        "focus": focus,
        "results": [],
    }


def search_knowledge_base(query):
    results = search(query, top_k=2)

    log(f"📚 Knowledge base search: {query}")
    for r in results:
        log(f"   {r['score']:.2f} - {r['source']} #{r['chunk_id']}")

    blocks = []
    for r in results:
        sourceFileName = r['source']
        chunkId        = r['chunk_id']
        chunkText      = r['text']

        header = f"[{sourceFileName} #{chunkId}]"
        block  = f"{header}\n{chunkText}"
        blocks.append(block)

    return "\n\n".join(blocks)



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
    {
        "type": "function",
        "function": {
            "name": "search_and_summarize",
            "description": "Search the web and summarize useful information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer"},
                    "focus": {"type": "string"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search the Zorvex Technologies company knowledge base: leave, medical, HR, hiring, tech, incidents, and other company related information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The users question, rewritten as a short, self contained query to search the knowledge base. The query should be concise and focused on the specific information the user is seeking.",
                    },
                },
                "required": ["query"],
            },
        },
    },
]

FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time": get_current_time,
    "calculate_sum": calculate_sum,
    "get_city_weather": get_city_weather,
    "search_and_summarize": search_and_summarize,
    "search_knowledge_base": search_knowledge_base,
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
