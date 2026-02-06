import sys
import os
import subprocess
import shlex
from typing import TypeAlias, Union

Response: TypeAlias = Union[str, False]


def exit(*args, **kwargs) -> Response:
    return False


def pwd(*args, **kwargs) -> Response:
    return os.getcwd()


def change_working_directory(*args, **kwargs) -> Response:
    target = args[1]

    target = os.path.expanduser(target)

    if not os.path.isdir(target):
        return f"cd: {target}: No such file or directory"

    os.chdir(target)


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


def read() -> list[str]:
    sys.stdout.write("$ ")
    raw_input = input()

    # Argument parsing
    parsed_input = shlex.split(s=raw_input)

    return parsed_input


def evaluate(args: list[str]) -> Response:
    # Evaluate input
    response = None
    first_command = args[0]
    if first_command in BUILTINS:
        response = BUILTINS[first_command](*args)

    elif find_executable_path(first_command):
        # If valid command and not a builtin
        # run and pass all args along
        full_command_path = find_executable_path(first_command)
        subprocess.run(args=args, executable=full_command_path)

    else:
        response = f"{first_command}: command not found"

    return response


BUILTINS: dict[str, Response] = {
    "exit": exit,
    "echo": echo,
    "type": type,
    "pwd": pwd,
    "cd": change_working_directory,
}


def main():
    args = read()

    response = evaluate(args=args)

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
