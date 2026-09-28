import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        # uncomment temperature for more deterministic output
        # temperature=0,
    )
    message = response.choices[0].message

    if response.usage is None:
        raise RuntimeError("No response, try again.")
    if args.verbose is True:
        print(f"User prompt:\n{args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    if message.tool_calls is not None:
        for tool_call in message.tool_calls:
            # function_args = json.loads(tool_call.function.arguments or "{}")
            result_message = call_function(tool_call, verbose=args.verbose)
            if args.verbose is True:
                print(f"-> {result_message['content']}")
    print(f"Response:\n{response.choices[0].message.content}")

if __name__ == "__main__":
    main()
