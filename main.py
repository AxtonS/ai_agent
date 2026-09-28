import argparse

# import json
from dotenv import load_dotenv

from call_bot import call_bot
from call_function import available_functions, call_function


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    response = call_bot(args, available_functions)
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
