import argparse

from env_var_helper import set_env_var


class ArgsParser:
    def __init__(self):
        self.args = None
        self.parser = argparse.ArgumentParser(description="Port Automation Script")
        self.subparsers = self.parser.add_subparsers(dest="command")
        self.add_arguments_for_commands()
        self.args = self.parser.parse_args()

    def execute_command(self):
        if self.args.command == "get_token":
            from port import get_port_token
            token = get_port_token(self.args.client_id, self.args.client_secret)
            set_env_var("PORT_TOKEN", token)
        elif self.args.command == "post_log":
            from port import post_log
            post_log(self.args.message, self.args.token, self.args.run_id)
        elif self.args.command == "create_environment":
            from port import create_environment
            create_environment(self.args.project, self.args.ttl, self.args.triggered_by)
        elif self.args.command == "add_ec2_to_environment":
            from port import add_ec2_to_environment
            add_ec2_to_environment()
        else:
            print("Invalid command")

    def add_arguments_for_commands(self):
        self._get_token_args()
        self._post_log_args()
        self._create_environment_args()
        self._add_ec2_to_environment_args()

    def _create_environment_args(self):
        create_env_parser = self.subparsers.add_parser("create_environment")
        create_env_parser.add_argument("--project", required=False, help="Project name")
        create_env_parser.add_argument("--token", required=False, help="PORT JWT token")
        create_env_parser.add_argument("--ttl", required=False, help="ttl of the ENV")
        create_env_parser.add_argument("--triggered_by", required=False, help="who triggered deployment userIdentifier")

    def _add_ec2_to_environment_args(self):
        create_env_parser = self.subparsers.add_parser("add_ec2_to_environment")
        create_env_parser.add_argument("--env", required=False, help="Env ID")
        create_env_parser.add_argument("--token", required=False, help="PORT JWT token")

    def _post_log_args(self):
        post_log_parser = self.subparsers.add_parser("post_log")
        post_log_parser.add_argument("--run_id", required=False, help="run_id of the action")
        post_log_parser.add_argument("--message", required=True, help="Log message to post")
        post_log_parser.add_argument("--token", required=False, help="PORT JWT token")

    def _get_token_args(self):
        get_token_parser = self.subparsers.add_parser("get_token")
        get_token_parser.add_argument("--client_id", required=True, help="Port client ID")
        get_token_parser.add_argument("--client_secret", required=True, help="Port client secret")
