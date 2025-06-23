import os

def write_file(working_directory, file_path, content):
    allowed_full_working_directory = os.path.abspath(working_directory)
    requested_file = os.path.abspath(os.path.join(working_directory, file_path if file_path else "."))
    if not requested_file.startswith(allowed_full_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        parent_dir = os.path.dirname(requested_file)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        with open(requested_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except FileExistsError as FEE:
        return f"Error: {FEE}"
    except Exception as e:
        return f"Error: {e}"