import argparse


class ArgsParser:
    def __init__(self):
        self.args = None
        self.parser = argparse.ArgumentParser(description="Port Automation Script")
        self.subparsers = self.parser.add_subparsers(dest="command")