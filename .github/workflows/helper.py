import json
import logging
import os
from datetime import datetime, timedelta
from typing import Optional

import pytz


def get_port_context():
    try:
        port_context_raw = get_env_var('PORT_CONTEXT')

        if not port_context_raw:
            logging.critical("PORT_CONTEXT environment variable is not set or empty.")
            raise RuntimeError("PORT_CONTEXT environment variable is not set or empty.")

        parsed_port_context = json.loads(
            port_context_raw.replace("\\", '').replace('"{', '{').replace('}"', '}'))

        return parsed_port_context

    except json.JSONDecodeError as e:
        logging.critical(f"Invalid JSON format in PORT_CONTEXT: {e}")
        return None
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        return None

def calculate_time_delta(time_input: str) -> str:

    current_time = datetime.now(pytz.UTC).replace(microsecond=0)

    # Parse and add time delta
    if time_input == "1 Day":
        future_time = current_time + timedelta(days=1)
    elif time_input == "2 Hours":
        future_time = current_time + timedelta(hours=2)
    elif time_input == "1 Week":
        future_time = current_time + timedelta(weeks=1)
    elif time_input == "Indefinite":
        future_time = current_time + timedelta(days=365)
    else:
        raise ValueError(f"Unsupported time input: {time_input}")

    # Convert to ISO 8601 format with milliseconds and Z for UTC
    return future_time.isoformat().replace('+00:00', '.000Z')

def get_env_var(var_name: str) -> Optional[str]:
    try:
        value = os.getenv(var_name, default=None)
        if value is not None:
            logging.info(f"Environment variable '{var_name}' found with value: {value}")
            return value
        else:
            logging.warning(f"Environment variable '{var_name}' not found.")
            return None
    except Exception as e:
        logging.error(f"Error retrieving environment variable '{var_name}': {e}")
        return None

def set_env_var(name: str, value: str):
    """Writes an environment variable to GITHUB_ENV for subsequent steps."""
    os.environ[name] = value
    github_env = os.getenv('GITHUB_ENV', default=None)
    if github_env:
        with open(github_env, 'a') as env_file:
            logging.info(f"Setting environment variable '{name}' in GITHUB_ENV.")
            env_file.write(f"{name}={value}\n")
        test = get_env_var('PORT_TOKEN')
        logging.info(f"===PORT_TOKEN = {test}")
    else:
        raise RuntimeError("GITHUB_ENV is not available. Are you running in a GitHub Actions environment?")