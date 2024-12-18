import json
import logging
import os
from datetime import datetime, timedelta
import pytz

def sanitize_to_json(input_string: str) -> str:
    """
    Attempts to sanitize a malformed JSON-like string into valid JSON format.

    Args:
        input_string (str): The input string to sanitize.

    Returns:
        str: A sanitized JSON string.
    """
    try:
        # Replace single quotes with double quotes and fix JSON-like syntax issues
        sanitized_string = (
            input_string
            .replace("'", '"')  # Replace single quotes with double quotes
            .replace(": ", ":")  # Remove extra spaces after colons
        )
        return sanitized_string
    except Exception as e:
        logging.error(f"Error sanitizing string: {e}")
        return input_string


def get_port_context():
    """
    Retrieves the PORT_CONTEXT from the environment variable.

    Returns:
        The PORT_CONTEXT as a dictionary, or None if the environment variable is not set or invalid.
    """
    try:
        port_context = os.environ['PORT_CONTEXT']  # Get the raw string
        logging.info(f"Raw PORT_CONTEXT: {port_context}")

        # Attempt to sanitize the input
        sanitized_port_context = sanitize_to_json(port_context)
        logging.info(f"Sanitized PORT_CONTEXT: {sanitized_port_context}")

        # Parse sanitized JSON
        return json.loads(sanitized_port_context)
    except KeyError:
        logging.error("PORT_CONTEXT environment variable is not set.")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON format in PORT_CONTEXT: {e}")
        return None

def calculate_time_delta(time_input: str) -> str:
    """
    Calculate future timestamp based on input string.

    Args:
        time_input (str): Time delta specification

    Returns:
        str: ISO 8601 formatted timestamp in UTC

    Supported inputs:
    - "1 Day"
    - "2 Hours"
    - "1 Week"
    - "Indefinite"
    """
    # Get current time in UTC
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