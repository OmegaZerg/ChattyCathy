import os
import subprocess

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