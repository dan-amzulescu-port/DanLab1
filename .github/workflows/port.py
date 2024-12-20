import logging
import os
from typing import Optional

import requests

from args_setup import create_environment_args
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


#
def create_environment(project: str = '', ttl: str = '', triggered_by: str = ''):
#     """
#     Create an environment entity in Port.
    port_env_context = get_port_context()
    try:
        url = f"{PORT_API_URL}/blueprints/environment/entities"
        headers = get_port_api_headers()

        project = port_env_context["inputs"]["project"].get("identifier", project)
        triggered_by = port_env_context.get("triggered_by", triggered_by)
        ttl = calculate_time_delta(port_env_context["inputs"].get("ttl", ttl))

        params = {"run_id": port_env_context["runId"], "upsert": "true"}

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
    port_env_context = get_port_context()
    

def create_ec2_cloud_resource(project, resource_type, token):
    """
    Create a cloud resource entity in Port.
    """
    url = f"{PORT_API_URL}/blueprints/cloudResource/entities"

    port_env_context = get_port_context()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    params = {
        "run_id": port_env_context["runId"],
        "upsert": "true"
    }
    data = {
        "identifier": f"{resource_type}_{os.urandom(4).hex()}",
        "title": f"{resource_type.capitalize()} Resource",
        "properties": {
            "kind": resource_type,
            "region": "us-east-1",  # Example region
            "status": "provisioning"
        },
        "relations": {
            "environment": [project]
        }
    }

    response = send_post_request(url, headers, params, data)

    if response:
        logging.info("Successfully created cloud resource: %s", data["identifier"])

def create_s3_cloud_resource(project, resource_type, token):
    """
    Create a cloud resource entity in Port.
    """
    url = f"{PORT_API_URL}/blueprints/cloudResource/entities"
    port_env_context = get_port_context()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    params = {
        "run_id": port_env_context["runId"],
        "upsert": "true"
    }
    data = {
        "identifier": f"{resource_type}_{os.urandom(4).hex()}",
        "title": f"{resource_type.capitalize()} Resource",
        "properties": {
            "kind": resource_type,
            "region": "us-east-1",  # Example region
            "status": "provisioning"
        },
        "relations": {
            "environment": [project]
        }
    }

    response = send_post_request(url, headers, params, data)

    if response:
        logging.info("Successfully created cloud resource: %s", data["identifier"])