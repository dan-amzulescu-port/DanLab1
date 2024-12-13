import json
import logging
import os

import requests
from constants import PORT_API_URL

def send_post_request(url, headers, data):
    """
    Helper function to send POST requests and handle errors.
    """
    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        logging.error("Failed to send POST request: %s", response.text)
        return None

    return response

def get_token(client_id, client_secret):
    """
    Retrieve the PORT JWT Token using the provided client credentials.
    """
    logging.info(f"url = {PORT_API_URL}/auth/access_token")
    url = f"{PORT_API_URL}/auth/access-token"
    data = {"clientId": client_id, "clientSecret": client_secret}
    response = send_post_request(url, {"Content-Type": "application/json"}, data)

    if response is None:
        return None

    return response.json().get("accessToken")

def post_log(port_context, message, token):
    """
    Post a log entry to Port.
    """
    run_id = json.loads(port_context).get("runId")
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
def create_environment(project, token, ttl):
#     """
#     Create an environment entity in Port.

    url = f"{PORT_API_URL}/blueprints/environment/entities"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "identifier": f"environment_{os.urandom(4).hex()}",
        "title": "Environment",
        "properties": {
            "time_bounded": True,
            "ttl": "2024-12-13T22:50:00.000Z"  # Example default TTL
        },
        "relations": {
            "project": [project]
        }
    }

    response = send_post_request(url, headers, data)

    if response:
        logging.info("Successfully created environment: %s", data["identifier"])

def create_cloud_resource(project, resource_type, token):
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