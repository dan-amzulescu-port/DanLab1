import json
import logging
import os
import re
from datetime import datetime, timedelta
from typing import Optional

import pytz


def sanitize_to_json(raw_context: str) -> str:
    """
    Converts a malformed JSON-like string into valid JSON.

    Args:
        raw_context (str): The malformed JSON-like string.

    Returns:
        str: A valid JSON string.
    """
    # Remove single quotes wrapping the entire string
    if raw_context.startswith("'") and raw_context.endswith("'"):
        raw_context = raw_context[1:-1]

    # Replace single quotes with double quotes
    sanitized = raw_context.replace("'", '"')

    # Enclose unquoted keys and values with double quotes
    sanitized = re.sub(r'(\b[a-zA-Z0-9_]+\b):', r'"\1":', sanitized)
    sanitized = re.sub(r':\s*([a-zA-Z0-9_.+-]+)', r': "\1"', sanitized)

    # Correct specific JSON formatting issues
    sanitized = sanitized.replace(': "true"', ': true')
    sanitized = sanitized.replace(': "false"', ': false')
    sanitized = sanitized.replace(': "null"', ': null')

    # Ensure properly formatted date strings
    sanitized = re.sub(r'"([0-9]{4}-[0-9]{2}-[0-9]{2})-([0-9T:.Z]+)"', r'"\1T\2"', sanitized)

    return sanitized


def get_port_context():
    try:
        port_context_raw = get_env_var('PORT_CONTEXT')

        if not port_context_raw:
            logging.critical("PORT_CONTEXT environment variable is not set or empty.")
            return None

        parsed_port_context = json.loads(sanitize_to_json(port_context_raw))
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
    github_env = os.getenv('GITHUB_ENV', default=None)
    if github_env:
        with open(github_env, 'a') as env_file:
            env_file.write(f"{name}={value}\n")
    else:
        raise RuntimeError("GITHUB_ENV is not available. Are you running in a GitHub Actions environment?")