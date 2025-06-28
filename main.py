import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
 
    #Used for command line execution
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python3 main.py "your prompt here" [--verbose]')
        print('Example: python3 main.py "How do I fix the calculator?"')
        sys.exit(1)

    user_prompt = " ".join(args)
    print("Hello from ChattyCathy! I am your AI assistant.")
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    #Used for interactive program
    # print("Hello from ChattyCathy! I am your AI assistant. Type 'quit' to exit.")
    # user_prompt = input("Enter a prompt to get started: ")
    # if user_prompt == "quit":
    #     print("Thanks for chatting. Talk to you next time!")
    #     sys.exit(0)

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    def call_function(function_call_part, verbose=False):
        functions = {"get_files_info": get_files_info, "get_file_content": get_file_content, "run_python_file": run_python_file, "write_file": write_file}

        if verbose:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        else: print(f" - Calling function: {function_call_part.name}")

        if function_call_part.name in functions:
            function = functions[function_call_part.name]
            arguments = {"working_directory": "./calculator"}
            arguments.update(function_call_part.args)
            function_result = function(**arguments)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": function_result},
                    )
                ],
            )
        else:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )

    def generate_content(client, messages, verbose):
        i = 0
        called = True
        while i < 20 and called:
            response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
            )
            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)
            function_calls = response.function_calls
            if function_calls:
                for function_call_part in function_calls:
                    function_call_result = call_function(function_call_part, verbose)
                    messages.append(function_call_result)
                    if not function_call_result.parts[0].function_response.response:
                        raise Exception("Content is missing from the call_function return, Red Alert!")
                    elif verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                called = False            
                if verbose:
                    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                    print("Response tokens:", response.usage_metadata.candidates_token_count)
                print("Response:")
                print(response.text)
            i += 1

    generate_content(client, messages, verbose)

if __name__ == "__main__":
    main()
