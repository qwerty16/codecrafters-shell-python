import sys
import os
import subprocess

BUILTINS = ["exit", "echo", "type", "pwd"]


def find_executable_path(command: str):
    # Check for being in builtins
    if command in BUILTINS:
        return command

    search_paths = os.environ["PATH"].split(os.pathsep)

    for search_path in search_paths:
        possible_file = os.path.join(search_path, command)

        if os.path.isfile(possible_file) and os.access(possible_file, os.X_OK):
            return possible_file

    return False


def main():
    sys.stdout.write("$ ")

    # Read
    raw_input = input()

    # Evaluate input
    response = None

    args = raw_input.split()
    first_command = args[0]

    full_command_path = find_executable_path(first_command)

    match full_command_path:
        case False:
            response = f"{first_command}: command not found"
        case "exit":
            # Check for early exit
            return False
        case "echo":
            # Echo all other args
            response = " ".join(args[1:])
        case "type":
            second_command = args[1]
            executable_found = find_executable_path(second_command)
            if second_command == executable_found:
                response = f"{second_command} is a shell builtin"
            elif executable_found:
                response = f"{second_command} is {executable_found}"
            else:
                response = f"{second_command}: not found"
        case "pwd":
            response = os.getcwd()
        case _:
            # If valid command and not a builtin
            # run and pass all args along
            subprocess.run(args=args, executable=full_command_path)

    # Print response
    if response is not None:
        print(response)

    return True


if __name__ == "__main__":

    continue_running = True
    while continue_running:
        continue_running = main()
