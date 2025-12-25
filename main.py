import sys
from formbricks.cli import handle_formbricks_command

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py formbricks <up|down|generate|seed>")
        sys.exit(1)

    domain = sys.argv[1]
    command = sys.argv[2]

    if domain != "formbricks":
        print(f"Unknown domain: {domain}")
        sys.exit(1)

    handle_formbricks_command(command)

if __name__ == "__main__":
    main()
