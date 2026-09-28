import os

from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the contents of a specified file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file to read content from",
                },
            "required": ["file_path"]
            },
        },
    },
}

def get_file_content(working_dir: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_dir)

        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            content = ""
            with open(target_file, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                content += file_content_string
                if f.read(1):
                    content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return content

    except OSError as e:
        return f"Error: {e}"
