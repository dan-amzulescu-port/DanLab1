import logging

from args_setup import add_arguments_for_commands, execute_command
from args_parser import ArgsParser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    args_parser = ArgsParser()
    add_arguments_for_commands(args_parser.subparsers)
    args = args_parser.parser.parse_args()
    execute_command(args)


if __name__ == "__main__":
    main()
