import argparse
from port import (add_ec2_to_environment, create_environment, post_log, get_port_token, create_k8s_cluster,
                  restart_workload, get_logs_workload, resize_workload)
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
            token = get_port_token(self.args.client_id, self.args.client_secret)
            set_env_var("PORT_TOKEN", token)
        elif self.args.command == "post_log":
            post_log(self.args.message, self.args.token, self.args.run_id)
        elif self.args.command == "create_environment":
            create_environment(self.args.project, self.args.ttl, self.args.triggered_by)
        elif self.args.command == "add_ec2_to_environment":
            add_ec2_to_environment()
        elif self.args.command == "create_k8s_cluster":
            create_k8s_cluster(self.args.project, self.args.ttl, self.args.triggered_by)
        elif self.args.command == "restart_workload":
            restart_workload()
        elif self.args.command == "get_logs_workload":
            get_logs_workload()
        elif self.args.command == "resize_workload":
            resize_workload(self.args.cpu_req, self.args.cpu_lim ,self.args.mem_req, self.args.mem_lim)
        else:
            print("Invalid command")

    def add_arguments_for_commands(self):
        self._get_token_args()
        self._post_log_args()
        self._create_environment_args()
        self._add_ec2_to_environment_args()
        self._create_k8s_cluster()
        self._restart_workload()
        self._resize_workload()
        self._get_logs_workload()

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

    def _create_k8s_cluster(self):
        create_env_parser = self.subparsers.add_parser("create_k8s_cluster")
        create_env_parser.add_argument("--token", required=False, help="PORT JWT token")
        create_env_parser.add_argument("--project", required=False, help="Project name")
        create_env_parser.add_argument("--ttl", required=False, help="ttl of the ENV")
        create_env_parser.add_argument("--triggered_by", required=False, help="who triggered deployment userIdentifier")

    def _restart_workload(self):
        create_env_parser = self.subparsers.add_parser("restart_workload")
        create_env_parser.add_argument("--token", required=False, help="PORT JWT token")

    def _resize_workload(self):
        create_env_parser = self.subparsers.add_parser("resize_workload")
        create_env_parser.add_argument("--token", required=False, help="PORT JWT token")

    def _get_logs_workload(self):
        create_env_parser = self.subparsers.add_parser("get_logs_workload")
        create_env_parser.add_argument("--token", required=False, help="PORT JWT token")