import logging
import os
import json

import requests
from constants import PORT_API_URL
from helper import calculate_time_delta, get_port_context


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

def get_token(client_id, client_secret):
    """
    Retrieve the PORT JWT Token using the provided client credentials.
    """
    url = f"{PORT_API_URL}/auth/access_token"
    data = {"clientId": client_id, "clientSecret": client_secret}
    response = send_post_request(url, {"Content-Type": "application/json"}, data)

    env_input = os.environ.get('JSON_INPUT')
    logging.info(f"Type of env_input: {type(env_input)} ->  {env_input}")
    cleaned_input = env_input.strip('"').replace('\\"', '"')
    logging.info(f"Type of cleaned_input: {type(cleaned_input)} ->  {cleaned_input}")
    cleaned_jsoned_input = json.loads(cleaned_input)
    logging.info(f"Type of cleaned_input: {type(cleaned_jsoned_input)} ->  {cleaned_jsoned_input}")
    '''
    port_context = get_port_context()

    logging.info(f"PORT_CONTEXT: {port_context}")
    if isinstance(port_context, dict):
        if 'inputs' in port_context:
            logging.info(f"context inputs = {port_context['inputs']}")
        else:
            logging.error("'inputs' key is missing in PORT_CONTEXT.")
    else:
        logging.error("PORT_CONTEXT is not a valid dictionary.")

    if response is None:
        return None

    with open(os.environ['GITHUB_ENV'], 'a') as env_file:
        env_file.write(f"PORT_TOKEN={response.json().get("accessToken")}\n")
    '''
    return response.json().get("accessToken")

def post_log(message, token, run_id):
    """
    Post a log entry to Port.
    """
    url = f"{PORT_API_URL}/actions/runs/{run_id}/logs"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {"message": message}
    response = send_post_request(url, headers, data)

    if response:
        logging.info("Successfully posted log: %s", message)

#
def create_environment(project: str = '', token: str = '', ttl: str = '', triggered_by: str = ''):
#     """
#     Create an environment entity in Port.

    url = f"{PORT_API_URL}/blueprints/environment/entities"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    if ttl == "Indefinite":
        time_bounded = False
    else:
        time_bounded = True
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