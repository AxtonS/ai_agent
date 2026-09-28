import os

from openai import OpenAI


def call_bot(args, available_functions, messages):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        # uncomment temperature for more deterministic output
        # temperature=0,
    )
    return response

