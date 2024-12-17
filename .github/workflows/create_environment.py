import logging
from args_setup import (print_inputs_args, get_token_args, post_log_args, create_environment_args,
                        create_cloud_resource_args)

from port import get_token, post_log, create_environment, create_cloud_resource
from args_parser import ArgsParser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def print_inputs(port_context, requires_s3, requires_ec2, project, ttl):
    """
    Print all provided inputs for debugging purposes.
    """
    logging.info("Printing all inputs provided:")
    logging.info(f"Port Context: {port_context}")
    logging.info(f"Requires S3: {requires_s3}")
    logging.info(f"Requires EC2: {requires_ec2}")
    logging.info(f"Project: {project}")
    logging.info(f"TTL: {ttl}")

def main():
    args_parser = ArgsParser()
    add_arguments_for_commands(args_parser.subparsers)
    args = args_parser.parser.parse_args()

    print (execute_command(args))



def execute_command(args):
    match args.command:
        case "print_inputs":
            print_inputs(args.port_context, args.requires_s3, args.requires_ec2, args.project, args.ttl)
        case "get_token":
            return get_token(args.client_id, args.client_secret)
        case "post_log":
            post_log(args.port_context, args.message, args.token)
        case "create_environment":
            create_environment(args.project, args.token, args.ttl, args.triggered_by)
        case "create_cloud_resource":
            create_cloud_resource(args.project, args.resource_type, args.token)
        case _:
            print("Invalid command")


def add_arguments_for_commands(subparsers):
    # Subcommand: print_inputs
    print_inputs_args(subparsers)
    # Subcommand: get_token
    get_token_args(subparsers)
    # Subcommand: post_log
    post_log_args(subparsers)
    # Subcommand: create_environment
    create_environment_args(subparsers)
    # Subcommand: create_cloud_resource
    create_cloud_resource_args(subparsers)


if __name__ == "__main__":
    main()
