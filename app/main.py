import sys
import os
import subprocess
from typing import TypeAlias, Union

Response: TypeAlias = Union[str, False]


def exit(*args, **kwargs) -> Response:
    return False


def pwd(*args, **kwargs) -> Response:
    return os.getcwd()


def echo(*args, **kwargs) -> Response:
    return " ".join(args[1:])


def type(*args, **kwargs) -> Response:
    second_command = args[1]
    executable_found = find_executable_path(second_command)

    if second_command in BUILTINS:
        return f"{second_command} is a shell builtin"
    elif executable_found:
        return f"{second_command} is {executable_found}"
    else:
        return f"{second_command}: not found"


def find_executable_path(command: str):
    search_paths = os.environ["PATH"].split(os.pathsep)

    for search_path in search_paths:
        possible_file = os.path.join(search_path, command)

        if os.path.isfile(possible_file) and os.access(possible_file, os.X_OK):
            return possible_file

    return False


BUILTINS: dict[str, Response] = {"exit": exit, "echo": echo, "type": type, "pwd": pwd}


def main():
    # Read
    sys.stdout.write("$ ")
    raw_input = input()

    args = raw_input.split()
    first_command = args[0]

    # Evaluate input
    response = None
    if first_command in BUILTINS:
        response = BUILTINS[first_command](*args)

    elif find_executable_path(first_command):
        # If valid command and not a builtin
        # run and pass all args along
        full_command_path = find_executable_path(first_command)
        subprocess.run(args=args, executable=full_command_path)

    else:
        response = f"{first_command}: command not found"

    # Print
    if response:
        print(response)

    # Loop if response is not False
    if response is False:
        return False

    return True


if __name__ == "__main__":
    continue_running = True
    while continue_running:
        continue_running = main()
