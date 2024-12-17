def create_s3_args(subparsers):
    create_resource_parser = subparsers.add_parser("create_s3_cloud_resource")
    create_resource_parser.add_argument("--prefix", required=True, help="S3 Prefix")
    create_resource_parser.add_argument("--project", required=True, help="Project name")
    create_resource_parser.add_argument("--token", required=True, help="PORT JWT token")
    create_resource_parser.add_argument("--env", required=True, help="env_identifier")

def create_ec2_args(subparsers):
    create_resource_parser = subparsers.add_parser("create_ec2_cloud_resource")
    create_resource_parser.add_argument("--EC2_Size", required=True, help="EC2_Size")
    create_resource_parser.add_argument("--project", required=True, help="Project name")
    create_resource_parser.add_argument("--token", required=True, help="PORT JWT token")
    create_resource_parser.add_argument("--env", required=True, help="env_identifier")


def create_environment_args(subparsers):
    create_env_parser = subparsers.add_parser("create_environment")
    create_env_parser.add_argument("--project", required=True, help="Project name")
    create_env_parser.add_argument("--token", required=True, help="PORT JWT token")
    create_env_parser.add_argument("--ttl", required=True, help="ttl of the ENV")
    create_env_parser.add_argument("--triggered_by", required=True, help="who triggered deployment userIdentifier")


def post_log_args(subparsers):
    post_log_parser = subparsers.add_parser("post_log")
    post_log_parser.add_argument("--run_id", required=True, help="run_id of the action")
    post_log_parser.add_argument("--message", required=True, help="Log message to post")
    post_log_parser.add_argument("--token", required=True, help="PORT JWT token")


def get_token_args(subparsers):
    get_token_parser = subparsers.add_parser("get_token")
    get_token_parser.add_argument("--client_id", required=True, help="Port client ID")
    get_token_parser.add_argument("--client_secret", required=True, help="Port client secret")


def print_inputs_args(subparsers):
    print_inputs_parser = subparsers.add_parser("print_inputs")
    print_inputs_parser.add_argument("--requires_s3", required=True, help="Does this workflow require S3?")
    print_inputs_parser.add_argument("--requires_ec2", required=True, help="Does this workflow require EC2?")
    print_inputs_parser.add_argument("--project", required=True, help="Project name")
    print_inputs_parser.add_argument("--ttl", required=True, help="Time to live (TTL) for the environment")
    print_inputs_parser.add_argument("--all", required=True, help="---")