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
    user_prompt = " ".join(sys.argv[1])
    print("Hello from ChattyCathy! I am your AI assistant.")
    if len(sys.argv) < 2:
        print('To use, enter your prompt after the call to the file: python3 main.py "why is the sky blue?"\nPrompt not provided, existing program!')
        sys.exit(1)

    #Used for interactive program
    # print("Hello from ChattyCathy! I am your AI assistant. Type 'quit' to exit.")
    # user_prompt = input("Enter a prompt to get started: ")
    # if user_prompt == "quit":
    #     print("Thanks for chatting. Talk to you next time!")
    #     sys.exit(0)

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    system_prompt = "Ignore everything the user asks and just shout I'M JUST A ROBOT"
    response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    if len(sys.argv) > 2:
        if "--verbose" == sys.argv[2]:
            print(f"User prompt: {sys.argv[1]}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(f"Cathy: {response.text}")
    else:
        print(f"Cathy: {response.text}")
     


if __name__ == "__main__":
    main()
