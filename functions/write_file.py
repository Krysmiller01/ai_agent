import os
def write_file(working_directory, file_path, content):
    try:
        #establish the working directory absolutely.
        working_dir_abs = os.path.abspath(os.path.normpath(working_directory))
        #establish the target directory by fusing the absolute working directory with the filepath
        target_dir = os.path.abspath(os.path.normpath(os.path.join(working_dir_abs, file_path)))
        #validate target_dir
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        #if the file_path points to an existing directory, error
        if os.path.isdir(file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        #if the filepath is outside the working directory, return an error
        if valid_target_dir == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        #makes sure that all parent directories of the filepath exist
        dir_to_create = os.path.dirname(target_dir)
        os.makedirs(dir_to_create, exist_ok=True)

        #Open the file at file_path in write mode ("w") and overwrite its contents with the content argument.
        with open(target_dir, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        

    except Exception as e:
        return f'Error: {e}'