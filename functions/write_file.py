import os
from google.genai import types
def write_file(working_directory, file_path, content):
    try:
        #establish the working directory absolutely.
        working_dir_abs = os.path.abspath(os.path.normpath(working_directory))
        #establish the target directory by fusing the absolute working directory with the filepath
        abs_file_path = os.path.abspath(os.path.normpath(os.path.join(working_dir_abs, file_path)))
        #validate abs_file_path
        valid_abs_file_path = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs
        #if the file_path points to an existing directory, error
        if os.path.isdir(file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        #if the filepath is outside the working directory, return an error
        if valid_abs_file_path == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        #makes sure that all parent directories of the filepath exist
        dir_to_create = os.path.dirname(abs_file_path)
        os.makedirs(dir_to_create, exist_ok=True)

        #Open the file at file_path in write mode ("w") and overwrite its contents with the content argument.
        with open(abs_file_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        

    except Exception as e:
        return f'Error: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes specified content to a file at a given path, creating the file and any necessary directories if they do not exist",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type =types.Type.STRING,
                description="The text content to be written into the file",
            ),
        },
        required=["file_path", "content"],
    ),
)

