import os
import subprocess
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
            capture_output = True,
            text = True,
            timeout=30
        )
        parts = []
        if result.returncode != 0:
            parts.append(f'Process exited with code {result.returncode}')
        if not result.stdout and not result.stderr:
            parts.append("No output produced")
        if result.stdout:
            parts.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            parts.append(f"STDERR:\n{result.stderr}")
        return "\n".join(parts)
    except Exception as e:
        return f'Error: executing Python file: {e}'