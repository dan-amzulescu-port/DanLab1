import logging

from args_setup import add_arguments_for_commands, execute_command
from helper import set_env_var, get_env_var

from port import get_port_token, post_log, create_environment, create_ec2_cloud_resource, create_s3_cloud_resource
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
    execute_command(args)


if __name__ == "__main__":
    main()
