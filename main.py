import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompt import config


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Generate content using Gemini API")
    parser.add_argument("prompt", help="The user prompt for token generation")
    parser.add_argument(
        "--verbose", action="store_true", help="Show prompt and response tokens"
    )
    args = parser.parse_args()

    prompt = args.prompt
    generate_content(client, prompt, verbose=args.verbose)


def generate_content(client, prompt, verbose=False):
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages, config=config
    )
    if response.function_calls:
        print("Function Calls:")
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print(response.text)

    if verbose:
        print("==========Verbose Output==========")
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
