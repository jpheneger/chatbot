import subprocess
import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = abs_working_dir
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        files_info = []
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)
            file_size = 0
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"

MAX_CHARS=10000 

def get_file_content(working_directory, path):
    abs_working_dir = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(working_directory, path))
    if not target.startswith(abs_working_dir):
        return f'Error: Cannot read "{path}" as it is outside the permitted working directory'
    if os.path.isdir(target):
        return f'Error: File not found or is not a regular file: "{path}"'
    try:
        with open(target, "r") as file:
            content = file.read(MAX_CHARS)
            if len(content) == MAX_CHARS:
                content += f"[...File \"{path}\" truncated at {MAX_CHARS} characters]"
            return content
    except FileNotFoundError:
        print("Error: File not found.")
        return None

def run_python_file(working_directory, path):
    abs_working_dir = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(working_directory, path))
    if not target.startswith(abs_working_dir):
        return f'Error: Cannot execute "{path}" as it is outside the permitted working directory'
    if not os.path.exists(target):
        return f'Error: File "{path}" not found.'
    file_name, file_extension = os.path.splitext(target)
    if not file_extension == '.py':
        return f'Error: "{path}" is not a Python file.'
    
    try:
        result = subprocess.run(["python3", target], cwd=working_directory, timeout=30, capture_output=True, text=True)
        if result.stdout != "":
            # print(f"STDOUT: {result.stdout}")
            return result
        elif result.stderr != "":
            # print(f"STDERR: {result.stderr}")
            return result
        else:
            print("No output produced.")
            return ""
    except subprocess.TimeoutExpired as e:
        print(f"Command timed out after {e.timeout} seconds")
        print("Captured output:", e.stdout)
        return f"Error: executing Python file: {e}"
    except subprocess.CalledProcessError as e:
        print(f"Process exited with code {e.returncode}")
        return f"Error: executing Python file: {e}"
    except Exception as e:
        return f"Error: executing Python file: {e}"

def write_file(working_directory, path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(working_directory, path))
    if not target.startswith(abs_working_dir):
        return f'Error: Cannot write to "{path}" as it is outside the permitted working directory'
    try:
        with open(target, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{target}" ({len(content)} characters written)'
    except Exception as e:
        err = f'Unable to write to "{target}": {e}'
        print(err)
        return err
    
def call_function(function_call_part, verbose=False):
    working_directory="./calculator"
    name=function_call_part.name
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"
    
    if verbose:
        print(f"Calling function: {function_call_part.name}({working_directory}, {function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    function_result = "?"
    match name:
        case "get_files_info":
            function_result = get_files_info(**args)
        case "get_file_content":
            function_result = get_file_content(**args)
        case "run_python_file":
            function_result = run_python_file(**args)
        case "write_file":
            function_result = write_file(**args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=name,
                        response={"error": f"Unknown function: {name}"},
                    )
                ],
            )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=name,
                response={"result": function_result},
            )
        ],
    )