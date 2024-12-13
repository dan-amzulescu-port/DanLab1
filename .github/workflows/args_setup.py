def create_cloud_resource_args(subparsers):
    create_resource_parser = subparsers.add_parser("create_cloud_resource")
    create_resource_parser.add_argument("--project", required=True, help="Project name")
    create_resource_parser.add_argument("--resource_type", required=True, help="Type of cloud resource (e.g., s3, ec2)")
    create_resource_parser.add_argument("--token", required=True, help="PORT JWT token")


def create_environment_args(subparsers):
    create_env_parser = subparsers.add_parser("create_environment")
    create_env_parser.add_argument("--project", required=True, help="Project name")
    create_env_parser.add_argument("--token", required=True, help="PORT JWT token")


def post_log_args(subparsers):
    post_log_parser = subparsers.add_parser("post_log")
    post_log_parser.add_argument("--port_context", required=True, help="Port context in JSON format")
    post_log_parser.add_argument("--message", required=True, help="Log message to post")
    post_log_parser.add_argument("--token", required=True, help="PORT JWT token")


def get_token_args(subparsers):
    get_token_parser = subparsers.add_parser("get_token")
    get_token_parser.add_argument("--client_id", required=True, help="Port client ID")
    get_token_parser.add_argument("--client_secret", required=True, help="Port client secret")


def print_inputs_args(subparsers):
    print_inputs_parser = subparsers.add_parser("print_inputs")
    print_inputs_parser.add_argument("--port_context", required=True, help="Port context in JSON format")
    print_inputs_parser.add_argument("--requires_s3", required=True, help="Does this workflow require S3?")
    print_inputs_parser.add_argument("--requires_ec2", required=True, help="Does this workflow require EC2?")
    print_inputs_parser.add_argument("--project", required=True, help="Project name")
    print_inputs_parser.add_argument("--ttl", required=True, help="Time to live (TTL) for the environment")
    print_inputs_parser.add_argument("--all", required=True, help="---")