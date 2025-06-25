import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
 
    #Used for command line execution
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
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

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    def generate_content(client, messages, verbose):
        response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )
        function_calls = response.function_calls
        if function_calls:
            for function_call_part in function_calls:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Response:")
        print(response.text)

    generate_content(client, messages, verbose)

if __name__ == "__main__":
    main()
