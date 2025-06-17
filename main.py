import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.schema import available_functions
from functions.functions import call_function

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

if len(sys.argv) == 2:
    user_prompt = sys.argv[1]
    flags = ""
    verbose=False
elif len(sys.argv) == 3:
    user_prompt = sys.argv[1]
    flags = sys.argv[2]
    if flags == "--verbose":
        verbose=True
    else:
        verbose=False
else:
    print("No prompt provided = exiting")
    sys.exit(1)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
model_name='gemini-2.0-flash-001'
messages = [
    types.Content(role="user", parts=[
        types.Part(text=user_prompt)
    ])
]

for i in range(20):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )
    
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: ")

    if response.candidates is not None:
        for candidate in response.candidates:
            # print(f"-----candidate: {candidate}")
            messages.append(candidate.content)

    if response.function_calls is not None:
        for function_call_part in response.function_calls:
            # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            function_call_result = call_function(function_call_part, verbose)

            messages.append(function_call_result)

            if function_call_result is None or function_call_result.parts is None or function_call_result.parts[0].function_response.response is None:
                raise Exception("invalid response")
            elif function_call_result.parts[0].function_response.response is not None and verbose == True:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                print(f" - Calling function: {function_call_part.name}")
            continue
    else:
        print(response.text)
        break