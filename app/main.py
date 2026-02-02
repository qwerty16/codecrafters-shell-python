import sys

def main():
    running = True

    while running:
        sys.stdout.write("$ ")

        # Read
        raw_input = input()

        # Evaluate input
        input_not_valid = True

        # Print response
        if input_not_valid:
            sys.stdout.write(f"{raw_input}: command not found\n")
        
        # Loop
        running = True


if __name__ == "__main__":
    main()
