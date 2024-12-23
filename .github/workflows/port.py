import logging
import os
from typing import Optional
import random
import requests

from constants import PORT_API_URL
from helper import calculate_time_delta, get_port_context, get_env_var


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


def create_environment(project: str = '', ttl: str = '', triggered_by: str = ''):
#     """
#     Create an environment entity in Port.

    port_env_context = get_port_context()
    try:

        url = f"{PORT_API_URL}/blueprints/environment/entities"
        headers = get_port_api_headers()
        params = {"run_id": port_env_context["runId"], "upsert": "true"}

        project = port_env_context["inputs"]["project"].get("identifier", project)
        triggered_by = port_env_context.get("triggered_by", triggered_by)
        ttl = calculate_time_delta(port_env_context["inputs"].get("ttl", ttl))

        data = {
            "identifier": f"environment_{os.urandom(4).hex()}",
            "title": "Environment",
            "properties": {
                "time_bounded": ttl != "Indefinite",
                "ttl": ttl  # Example default TTL
            },
            "relations": {
                "project": project,
                "triggered_by": triggered_by
            }
        }

        response = send_post_request(url, headers, params, data)

        if response:
            e_id = response.json()["entity"]["identifier"]
            logging.debug(f"Successfully created environment e_id: {e_id}")
            post_log(f'✅ Environment ({e_id}) successfully created! 🥳 Ready to deploy 🚀',
                     run_id=port_env_context["runId"])
            # create_environment_cloud_resources(env=e_id)
        else:
            logging.error("Environment creation failed. No valid 'identifier' in response.")
            post_log(f'❌ Failed to create environment.', run_id=port_env_context["runId"])

    except Exception as e:
        logging.error(f"Error occurred while creating environment: {str(e)}")
        post_log(f'❌ Error occurred while creating environment: {str(e)}', run_id=port_env_context["runId"])

def create_environment_cloud_resources(e_id: str):
    if not e_id:
        logging.error("Environment ID is not provided.")
        raise RuntimeError("Environment ID is not provided.")
    port_env_context = get_port_context()
    try:
        if port_env_context["inputs"].get("requires_ec_2", False):
            create_cloud_resource(e_id, "EC2")
        if port_env_context["inputs"].get("requires_s_3", False):
            create_cloud_resource(e_id, "S3")
    except Exception as e:
        logging.error(f"Error occurred while creating cloud resources: {str(e)}")
        post_log(f'❌ Error occurred while creating cloud resources: {str(e)}', run_id=port_env_context["runId"])


def create_cloud_resource(e_id:str = '', kind: str = ''):
    """
    Create a cloud resource entity (EC2 or S3) in Port.
    """
    logging.info(f"Creating cloud resource of kind: {kind}")
    port_env_context = get_port_context()
    try:

        url = f"{PORT_API_URL}/blueprints/cloudResource/entities"
        headers = get_port_api_headers()
        params = {"run_id": port_env_context["runId"], "upsert": "true"}

        project = port_env_context["inputs"]["project"].get("identifier", None)
        triggered_by = port_env_context.get("triggered_by", None)

        region = random.choice(["us-west-1", "us-east-1", "eu-central-1"])
        tags = { "Owner": triggered_by, "project": project}
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

        response = send_post_request(url, headers, params, data)
        logging.info(f"Response: {response}")
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
