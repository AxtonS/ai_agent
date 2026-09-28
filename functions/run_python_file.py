import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run the specified python file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The python file to run",
                },
                "args": {
                    "type": "array",
                    "items": {
                            "type": "string"
                    },
                    "description": "Optional arguments to be run with the python script",
                }
            },
            "required": ["file_path"]
        },
    },
}

def run_python_file(working_dir: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_dir)

        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif target_file[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args != None:
            command.extend(args)
        completed_process = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)

        output = ""
        if completed_process.returncode != 0:
            output += f"Process exited with code {completed_process.returncode}\n"
        if completed_process.stderr == "" and completed_process.stdout == "":
            output += "No output produced\n"
        else:
            output += f"STDOUT: {completed_process.stdout}\n"
            output += f"STDERR: {completed_process.stderr}\n"

        return output
    except OSError as e:
        return f"Error: executing Python file: {e}"
