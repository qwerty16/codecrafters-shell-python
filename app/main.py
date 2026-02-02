import sys

def main():
    sys.stdout.write("$ ")

    raw_input = input()

    input_not_valid = True

    if input_not_valid:
        sys.stdout.write(f"{raw_input}: command not found")
    pass


if __name__ == "__main__":
    main()
