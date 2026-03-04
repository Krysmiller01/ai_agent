import os
import subprocess
from google.genai import types
def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(os.path.normpath(working_directory))
        abs_file_path = os.path.abspath(os.path.normpath(os.path.join(working_dir_abs, file_path)))
        valid_abs_file_path = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs
        if valid_abs_file_path == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        path, extension = os.path.splitext(abs_file_path)
        if extension.lower() != '.py':
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", abs_file_path]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text = True,
            timeout=30
        )
        output = result.stdout or ""

        if result.returncode != 0:
            return f"process exited with code {result.returncode}\n{output}".strip()
        if output.strip() == "":
            return "No output produced"
        return output.strip()
    except Exception as e:
        return f'Error: executing Python file: {e}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python script at a specified path and returns its output (STDOUT and STDERR)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file (.py) to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of command-line arguments to pass to the script",
            ),
        },
        required=["file_path"],
    ),
)