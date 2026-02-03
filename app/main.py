import sys

BUILTINS = ["exit", "echo", "type"]


def main():
    sys.stdout.write("$ ")

    # Read
    raw_input = input()

    # Evaluate input
    response = None

    args = raw_input.split()
    first_command = args[0]

    match first_command:
        case "exit":
            # Check for early exit
            return False
        case "echo":
            # Echo all other args
            response = " ".join(args[1:])
        case "type":
            second_command = args[1]
            if second_command in BUILTINS:
                response = f"{second_command} is a shell builtin"
            else:
                response = f"{second_command}: not found"
        case _:
            response = f"{first_command}: command not found"

    # Print response
    print(response)

    return True


if __name__ == "__main__":
    continue_running = True
    while continue_running:
        continue_running = main()
