import logging
import os
import json
from typing import Optional
import base64

import requests
from constants import PORT_API_URL
from helper import calculate_time_delta, get_port_context, get_env_var


def send_post_request(url, headers, data):
    """
    Helper function to send POST requests and handle errors.
    """
    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200 and response.status_code != 201:
        logging.info("response.status_code: %s", response.status_code)
        logging.error("Failed to send POST request: %s", response.text)
        return None

    return response


def get_port_token(client_id:str = "", client_secret:str = "") -> Optional[str]:
    """
    Retrieve the PORT JWT Token using the provided client credentials.
    """
    url = f"{PORT_API_URL}/auth/access_token"
    client_id_from_env = os.environ.get('PORT_CLIENT_ID', None)
    client_secret_from_env = os.environ.get('PORT_CLIENT_SECRET', None)
    if client_id_from_env != client_id:
        logging.error(f"client_id_from_env({base64.b64encode(client_id_from_env.encode('utf-8')).decode('utf-8')}) != "
                      f"client_id({base64.b64encode(client_id.encode('utf-8')).decode('utf-8')})")
        if client_secret_from_env != client_secret:
            logging.error(f"client_secret_from_env({base64.b64encode(client_secret_from_env.encode('utf-8')).decode('utf-8')}) != "
                      f"client_secret({base64.b64encode(client_secret.encode('utf-8')).decode('utf-8')})")
        return None

    encoded_data = base64.b64encode(client_id.encode('utf-8')).decode('utf-8')
    logging.info(f"PORT_CLIENT_ID(len): {len(client_id)} - {encoded_data}")
    client_secret = os.environ.get('PORT_CLIENT_SECRET', None)

    encoded_data = base64.b64encode(client_secret.encode('utf-8')).decode('utf-8')
    logging.info(f"PORT_CLIENT_SECRET(len): {len(client_secret)} - {encoded_data}")

    data = {"clientId": client_id, "clientSecret": client_secret}
    response = send_post_request(url, {"Content-Type": "application/json"}, data)
    if response is None:
        logging.error("Failed to retrieve PORT JWT Token. (empty response)")
        return None

    return response.json().get("accessToken")


def get_env_var_context():
    return json.loads(os.environ.get('ENV_PORT_CONTEXT', None).strip('"').replace('\\"', '"'))


def post_log(message, token="", run_id=""):
    """
    Post a log entry to Port.
    """
    env_var_context = get_env_var_context()
    if not token:
        token = get_env_var("PORT_TOKEN")

    url = f"{PORT_API_URL}/actions/runs/{env_var_context["run_id"]}/logs"
    headers = get_port_api_headers(token)
    data = {"message": message}
    response = send_post_request(url, headers, data)

    if response:
        logging.info("Successfully posted log: %s", message)


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
def create_environment(project: str = '', token: str = '', ttl: str = '', triggered_by: str = ''):
#     """
#     Create an environment entity in Port.

    url = f"{PORT_API_URL}/blueprints/environment/entities"

    headers = get_port_api_headers(token)

    time_bounded = ttl != "Indefinite"

    ttl = calculate_time_delta(ttl)
    logging.info("ttl: %s", ttl)
    data = {
        "identifier": f"environment_{os.urandom(4).hex()}",
        "title": "Environment",
        "properties": {
            "time_bounded": time_bounded,
            "ttl": ttl  # Example default TTL
        },
        "relations": {
            "project": project,
            "triggered_by": triggered_by
        }
    }

    response = send_post_request(url, headers, data)

    if response:
        logging.info(f"Successfully created environment: {data["identifier"]}")
        logging.info(f"Successfully created environment response: {response}")
        logging.info(f"Successfully created environment e_id: {response.json()["entity"]["identifier"]}")


def create_ec2_cloud_resource(project, resource_type, token):
    """
    Create a cloud resource entity in Port.
    """
    url = f"{PORT_API_URL}/blueprints/cloudResource/entities"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
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

    response = send_post_request(url, headers, data)

    if response:
        logging.info("Successfully created cloud resource: %s", data["identifier"])

def create_s3_cloud_resource(project, resource_type, token):
    """
    Create a cloud resource entity in Port.
    """
    url = f"{PORT_API_URL}/blueprints/cloudResource/entities"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
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

    response = send_post_request(url, headers, data)

    if response:
        logging.info("Successfully created cloud resource: %s", data["identifier"])