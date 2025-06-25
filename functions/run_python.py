import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    allowed_full_working_directory = os.path.abspath(working_directory)
    requested_filepath = os.path.abspath(os.path.join(working_directory, file_path if file_path else "."))
    if not requested_filepath.startswith(allowed_full_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(requested_filepath):
        return f'Error: File "{file_path}" not found.'
    if not requested_filepath.endswith(".py"):
        return f'"{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(['python3', requested_filepath], timeout=30.0, capture_output=True, cwd=allowed_full_working_directory)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    if not result.stdout and not result.stderr:
        return "No output produced."
    if result.returncode == 0:
        return f'STDOUT: {result.stdout.decode()}\nSTDERR: {result.stderr.decode()}\n'
    else:
        return f'STDOUT: {result.stdout.decode()}\nSTDERR: {result.stderr.decode()}\nProcess exited with code {result.returncode}'
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)