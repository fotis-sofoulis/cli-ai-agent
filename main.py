import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions, call_function
from prompt import system_prompt


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
    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages, config=config
    )

    if verbose:
        print("==========Verbose Output==========")
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        print(response.text)

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")


if __name__ == "__main__":
    main()
