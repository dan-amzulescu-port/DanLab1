import logging

from helper import set_env_var
from port import get_port_token, post_log, create_environment


def execute_command(args):
    match args.command:
        case "get_token":
            set_env_var("PORT_TOKEN", get_port_token(args.client_id, args.client_secret))
        case "post_log":
            post_log(args.message, args.token, args.run_id)
        case "create_environment":
            return create_environment()
        case _:
            print("Invalid command")


def create_environment_args(subparsers):
    create_env_parser = subparsers.add_parser("create_environment")
    create_env_parser.add_argument("--project", required=False, help="Project name")
    create_env_parser.add_argument("--token", required=False, help="PORT JWT token")
    create_env_parser.add_argument("--ttl", required=False, help="ttl of the ENV")
    create_env_parser.add_argument("--triggered_by", required=False, help="who triggered deployment userIdentifier")


def post_log_args(subparsers):
    post_log_parser = subparsers.add_parser("post_log")
    post_log_parser.add_argument("--run_id", required=False, help="run_id of the action")
    post_log_parser.add_argument("--message", required=True, help="Log message to post")
    post_log_parser.add_argument("--token", required=False, help="PORT JWT token")


def get_token_args(subparsers):
    get_token_parser = subparsers.add_parser("get_token")
    get_token_parser.add_argument("--client_id", required=True, help="Port client ID")
    get_token_parser.add_argument("--client_secret", required=True, help="Port client secret")


def add_arguments_for_commands(subparsers):
    get_token_args(subparsers)
    post_log_args(subparsers)
    create_environment_args(subparsers)
