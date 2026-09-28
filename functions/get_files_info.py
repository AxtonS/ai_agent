import os


def get_files_info(working_dir: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_dir)

        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    except OSError as e:
        return f"Error: {e}"

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as  it is outside the permitted working directory'
    elif not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    else:
        contents = os.listdir(target_dir)
        name = directory
        if name == ".":
            name = "current"
        directory_contents = f"Result for {name} directory:\n"
        for item in contents:
            current_path = f"{target_dir}/{item}"
            try:
                size = os.path.getsize(current_path)
                is_dir = os.path.isdir(current_path)
                directory_contents += f"  - {item}: file_size={size} bytes, is_dir={is_dir}\n"
            except OSError as e:
                return f"Error: {e}"

        return directory_contents

