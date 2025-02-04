import logging
import os
from typing import Optional
import random
import requests

from constants import PORT_API_URL
from env_var_helper import get_port_context, get_env_var
from misc_helers import calculate_time_delta


def send_post_request(url, headers, params, data):
    """
    Helper function to send POST requests and handle errors.
    """
    response = requests.post(url, headers=headers, params=params, json=data)

    if response.status_code != 200 and response.status_code != 201:
        logging.error(f"Failed to send POST request: {response.text}:{response.status_code}")
        return None

    return response

def get_port_token(client_id:str = "", client_secret:str = "") -> Optional[str]:
    """
    Retrieve the PORT JWT Token using the provided client credentials.
    """
    url = f"{PORT_API_URL}/auth/access_token"

    data = {"clientId": client_id, "clientSecret": client_secret}
    response = send_post_request(url, {"Content-Type": "application/json"}, None,data)
    if response is None:
        logging.critical("Failed to retrieve PORT JWT Token. (empty response)")
        raise RuntimeError("Failed to retrieve PORT JWT Token.")

    return response.json().get("accessToken")

def post_log(message, token="", run_id=""):
    """
    Post a log entry to Port.
    """
    env_var_context = get_port_context()
    if not run_id:
        run_id = env_var_context["runId"]
    url = f'{PORT_API_URL}/actions/runs/{run_id}/logs'
    headers = get_port_api_headers(token)
    data = {"message": message}
    response = send_post_request(url, headers, None, data=data)

    if not response:
        logging.error(f"Error writing log message {message} to Port.")

def get_port_api_headers(token:str = ""):
    if not token:
        token = get_env_var("PORT_TOKEN")
        if not token:
            logging.error("PORT_TOKEN environment variable is not set or empty.")
            return None
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    return headers

def create_entity(blueprint: str, data: dict, upsert: bool = True):
    """
    Create an entity in Port.
    """
    port_env_context = get_port_context()
    try:
        url = f"{PORT_API_URL}/blueprints/{blueprint}/entities"
        headers = get_port_api_headers()
        params = {"run_id": port_env_context["runId"], "upsert": "true"} if upsert else None

        response = send_post_request(url, headers, params, data)

        if response:
            e_id = response.json()["entity"]["identifier"]
            logging.debug(f"Successfully created entity {e_id} in {blueprint} blueprint")
            post_log(f'✅ Successfully created entity {e_id} in {blueprint} blueprint! 🥳',
                     run_id=port_env_context["runId"])
            return response
        else:
            logging.error(f"entity creation in {blueprint} failed. No valid 'identifier' in response.")
            post_log(f'❌ Failed to create entity in {blueprint}.', run_id=port_env_context["runId"])
            raise RuntimeError(f"Failed to create entity in {blueprint}.")

    except Exception as e:
        logging.error(f"Error occurred while creating {blueprint}: {str(e)}")
        post_log(f'❌ Error occurred while creating {blueprint}: {str(e)}', run_id=port_env_context["runId"])
        raise RuntimeError(f"Error occurred while creating {blueprint}: {str(e)}")

def restart_workload():
    """
    Create a Kubernetes cluster entity in Port.
    """
    port_env_context = get_port_context()
    try:

        workload_name = port_env_context["inputs"].get("workload", "")


        post_log(f'fetching current status of the workload "{workload_name}" 🔍', run_id=port_env_context["runId"])
        post_log(f'restarting workload "{workload_name}" with rolling update 🔄', run_id=port_env_context["runId"])
        post_log(f'waiting for rollout to complete for workload "{workload_name}" ⏳', run_id=port_env_context["runId"])
        post_log(f'workload "{workload_name}" has been successfully restarted ✅', run_id=port_env_context["runId"])
        post_log(f'checking the updated status of workload "{workload_name}" 🆕', run_id=port_env_context["runId"])
        post_log(f'workload "{workload_name}" is now running successfully 🚀', run_id=port_env_context["runId"])
    except Exception as e:
        logging.error(f"Error occurred while restarting workload: {str(e)}")
        post_log(f'❌ Error occurred while restarting workload: {str(e)}', run_id=port_env_context["runId"])
        raise RuntimeError(f"Error occurred while restarting workload: {str(e)}")

def create_k8s_cluster(project: str = '', ttl: str = '', triggered_by: str = ''):
    """
    Create a Kubernetes cluster entity in Port.
    """
    port_env_context = get_port_context()
    try:
        project = port_env_context["inputs"]["project"].get("identifier", project)
        triggered_by = port_env_context.get("triggered_by", triggered_by)
        ttl = calculate_time_delta(port_env_context["inputs"].get("ttl", ttl))
        cluster_name_input = port_env_context["inputs"].get("cluster_name", "")
        cluster_rand = os.urandom(4).hex()
        cluster_name = f"{cluster_name_input}_{project}_{cluster_rand}"

        data = {
            "identifier": f"{cluster_name}",
            "title": cluster_name,
            "properties": {
                "time_bounded": ttl != "Indefinite",
                "ttl": ttl  # Example default TTL
            },
            "relations": {
                "project": project,
                "triggered_by": triggered_by
            }
        }

        response = create_entity("cluster", data, True)

        if response:

            post_log(f'eksctl version 0.194.0 🚀', run_id=port_env_context["runId"])
            post_log(f'using region us-east-1 🌍', run_id=port_env_context["runId"])
            post_log(f'setting availability zones to [us-east-1a us-east-1b] 🌐', run_id=port_env_context["runId"])
            post_log(f'subnets for us-east-1a - public:192.168.0.0/19 private:192.168.64.0/19 🏙️',
                     run_id=port_env_context["runId"])
            post_log(f'subnets for us-east-1b - public:192.168.32.0/19 private:192.168.96.0/19 🌆',
                     run_id=port_env_context["runId"])
            post_log(f'nodegroup "ng-598412f9" will use "" [AmazonLinux2/1.30] 🐧', run_id=port_env_context["runId"])
            post_log(f'using Kubernetes version 1.30 🧑‍💻', run_id=port_env_context["runId"])
            post_log(f'creating EKS cluster "{cluster_name}" in "us-east-1" region with managed nodes 🎉',
                     run_id=port_env_context["runId"])
            post_log(f'will create 2 separate CloudFormation stacks for cluster itself and the initial managed nodegroup 📦',
                     run_id=port_env_context["runId"])
            post_log(
                f'if you encounter any issues, check CloudFormation console or try "eksctl utils describe-stacks --region=us-east-1 --cluster={cluster_name}" 🛠️',
                run_id=port_env_context["runId"])
            post_log(
                f'Kubernetes API endpoint access will use default of {{publicAccess=true, privateAccess=false}} for cluster "{cluster_name}" in "us-east-1" 🌐',
                run_id=port_env_context["runId"])
            post_log(f'CloudWatch logging will not be enabled for cluster "{cluster_name}" in "us-east-1" 📉',
                     run_id=port_env_context["runId"])
            post_log(
                f'you can enable it with "eksctl utils update-cluster-logging --enable-types={{SPECIFY-YOUR-LOG-TYPES-HERE (e.g. all)}} --region=us-east-1 --cluster={cluster_name}" 🔧',
                run_id=port_env_context["runId"])
            post_log(f'default addons coredns, vpc-cni, kube-proxy were not specified, will install them as EKS addons 🛠️',
                     run_id=port_env_context["runId"])
            post_log(f'building cluster stack "eksctl-{cluster_name}-cluster" 🏗️', run_id=port_env_context["runId"])
            post_log(f'deploying stack "eksctl-{cluster_name}-cluster" 📤', run_id=port_env_context["runId"])
            post_log(f'waiting for CloudFormation stack "eksctl-{cluster_name}-cluster" ⏳',
                     run_id=port_env_context["runId"])
            post_log(f'creating addon ➕', run_id=port_env_context["runId"])
            post_log(f'successfully created addon ✅', run_id=port_env_context["runId"])
            post_log(
                f'recommended policies were found for "vpc-cni" addon, but since OIDC is disabled on the cluster, eksctl cannot configure the requested permissions 🚨',
                run_id=port_env_context["runId"])
            post_log(f'creating addon ➕', run_id=port_env_context["runId"])
            post_log(f'successfully created addon ✅', run_id=port_env_context["runId"])
            post_log(f'building managed nodegroup stack "eksctl-{cluster_name}-nodegroup-ng-598412f9" 🏗️',
                     run_id=port_env_context["runId"])
            post_log(f'deploying stack "eksctl-{cluster_name}-nodegroup-ng-598412f9" 📤', run_id=port_env_context["runId"])
            post_log(f'waiting for CloudFormation stack "eksctl-{cluster_name}-nodegroup-ng-598412f9" ⏳',
                     run_id=port_env_context["runId"])
            post_log(f'waiting for the control plane to become ready 🔄', run_id=port_env_context["runId"])
            post_log(f'saved kubeconfig as "/home/dan/.kube/config" 📄', run_id=port_env_context["runId"])
            post_log(f'all EKS cluster resources for "{cluster_name}" have been created 🎉',
                     run_id=port_env_context["runId"])
            post_log(f'created 1 managed nodegroup(s) in cluster "{cluster_name}" ✅', run_id=port_env_context["runId"])
            post_log(f'nodegroup "ng-598412f9" has 3 node(s) 🖥️', run_id=port_env_context["runId"])
            post_log(f'node "ip-192-168-15-185.ec2.internal" is ready ✅', run_id=port_env_context["runId"])
            post_log(f'node "ip-192-168-23-133.ec2.internal" is ready ✅', run_id=port_env_context["runId"])
            post_log(f'node "ip-192-168-63-179.ec2.internal" is ready ✅', run_id=port_env_context["runId"])
            post_log(f'waiting for at least 2 node(s) to become ready in "ng-598412f9" ⏳', run_id=port_env_context["runId"])
            post_log(f'kubectl command should work with "/home/dan/.kube/config", try "kubectl get nodes" 🖥️',
                     run_id=port_env_context["runId"])
            post_log(f'EKS cluster "{cluster_name}" in "us-east-1" region is ready 🎉', run_id=port_env_context["runId"])
        else:
            logging.error("Was not able to create K8s Cluster")
            post_log(f'❌ Failed to create K8s Cluster.', run_id=port_env_context["runId"])


    except Exception as e:
        logging.error(f"Error occurred while creating Kubernetes cluster: {str(e)}")
        post_log(f'❌ Error occurred while creating Kubernetes cluster: {str(e)}', run_id=port_env_context["runId"])
        raise RuntimeError(f"Error occurred while creating Kubernetes cluster: {str(e)}")

def create_environment(project: str = '', ttl: str = '', triggered_by: str = ''):
#     """
#     Create an environment entity in Port.

    port_env_context = get_port_context()
    try:
        project = port_env_context["inputs"]["project"].get("identifier", project)
        triggered_by = port_env_context.get("triggered_by", triggered_by)
        ttl = calculate_time_delta(port_env_context["inputs"].get("ttl", ttl))
        env_rand = os.urandom(4).hex()
        env_name = f"env_{env_rand}_{project}"

        data = {
            "identifier": f"environment_{env_rand}",
            "title": env_name,
            "properties": {
                "time_bounded": ttl != "Indefinite",
                "ttl": ttl  # Example default TTL
            },
            "relations": {
                "project": project,
                "triggered_by": triggered_by
            }
        }

        response = create_entity("environment", data, True)

        if response:
            e_id = response.json()["entity"]["identifier"]
            logging.debug(f"Successfully created environment e_id: {e_id}")
            post_log(f'✅ Environment ({e_id}) successfully created! 🥳 Ready to deploy 🚀',
                     run_id=port_env_context["runId"])
            create_environment_cloud_resources(e_id=e_id)
        else:
            logging.error("Environment creation failed. No valid 'identifier' in response.")
            post_log(f'❌ Failed to create environment.', run_id=port_env_context["runId"])

    except Exception as e:
        logging.error(f"Error occurred while creating environment: {str(e)}")
        post_log(f'❌ Error occurred while creating environment: {str(e)}', run_id=port_env_context["runId"])
        raise RuntimeError(f"Error occurred while creating environment: {str(e)}")

def create_environment_cloud_resources(e_id: str):
    port_env_context = get_port_context()
    try:
        if port_env_context["inputs"].get("requires_ec_2", False):
            create_cloud_resource(e_id, "EC2")
        if port_env_context["inputs"].get("requires_s_3", False):
            create_cloud_resource(e_id, "S3")
    except Exception as e:
        logging.error(f"Error occurred while creating cloud resources: {str(e)}")
        post_log(f'❌ Error occurred while creating cloud resources: {str(e)}', run_id=port_env_context["runId"])
        raise RuntimeError(f"Error occurred while creating cloud resources: {str(e)}")

def add_ec2_to_environment():
    """
    Add an EC2 instance to an environment in Port.
    """
    port_env_context = get_port_context()
    try:
        env_id = port_env_context["inputs"]["environment"].get("identifier", "")
        if not env_id:
            logging.error("Environment identifier not found in the context.")
            post_log(f'❌ Environment identifier not found in the context.', run_id=port_env_context["runId"])
            raise RuntimeError("Environment identifier not found in the context.")

        create_cloud_resource(e_id=env_id, kind="EC2")
    except Exception as e:
        logging.error(f"Error occurred while adding EC2 to environment: {str(e)}")
        post_log(f'❌ Error occurred while adding EC2 to environment: {str(e)}', run_id=port_env_context["runId"])
        raise RuntimeError(f"Error occurred while adding EC2 to environment: {str(e)}")

def create_cloud_resource(e_id:str = '', kind: str = ''):
    """
    Create a cloud resource entity (EC2 or S3) in Port.
    """
    logging.info(f"Creating cloud resource of kind: {kind}")
    port_env_context = get_port_context()
    try:
        triggered_by = port_env_context.get("triggered_by", None)

        region = random.choice(["us-west-1", "us-east-1", "eu-central-1"])
        tags = { "Owner": triggered_by, "Environment": e_id }
        link = f"https://{kind}.{region}.aws.com/resource"
        status = random.choice(["running", "stopped", "provisioning"])

        data = {
            "identifier": f"cloudResource_{kind}_{os.urandom(4).hex()}",
            "title": f"{kind} Resource",
            "properties": {
                "kind": kind,
                "region": region,
                "tags": tags,
                "link": link,
                "status": status
            },
            "relations": {
                "environment": e_id
            }
        }
        response = create_entity("cloudResource", data, True)

        if response:
            resource_id = response.json().get("entity", {}).get("identifier", "")
            if resource_id:
                logging.debug(f"Successfully created cloud resource with ID: {resource_id}")
                post_log(f'✅ Cloud resource ({resource_id}) successfully created! 🥳',
                         run_id=port_env_context["runId"])
            else:
                logging.error("Cloud resource creation failed. No valid 'identifier' in response.")
                post_log(f'❌ Failed to create cloud resource.', run_id=port_env_context["runId"])
        else:
            logging.error("Cloud resource creation failed. No response received.")
            post_log(f'❌ Failed to create cloud resource due to API error.', run_id=port_env_context["runId"])

    except Exception as e:
        logging.error(f"Error occurred while creating cloud resource: {str(e)}")
        post_log(f'❌ Error occurred while creating cloud resource: {str(e)}', run_id=port_env_context["runId"])
