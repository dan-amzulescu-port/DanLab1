import logging

from args_parser import ArgsParser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    args_parser = ArgsParser()
    args_parser.execute_command()

if __name__ == "__main__":
    main()
