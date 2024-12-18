import json
import logging
import os
import re
from datetime import datetime, timedelta
import pytz


def sanitize_to_json(raw_context: str) -> str:
    """
    Converts a malformed JSON-like string into valid JSON.

    Args:
        raw_context (str): The malformed JSON-like string.

    Returns:
        str: A valid JSON string.
    """
    # Remove the single quotes wrapping the entire string
    if raw_context.startswith("'") and raw_context.endswith("'"):
        raw_context = raw_context[1:-1]

    # Replace single quotes with double quotes
    sanitized = raw_context.replace("'", '"')

    # Enclose keys with double quotes
    sanitized = re.sub(r'(\b[a-zA-Z0-9_]+\b):', r'"\1":', sanitized)

    # Ensure "null", "true", and "false" are properly formatted
    sanitized = sanitized.replace(":null", ": null")
    sanitized = sanitized.replace(":true", ": true")
    sanitized = sanitized.replace(":false", ": false")

    return sanitized



def get_port_context():
    """
    Retrieves the PORT_CONTEXT from the environment variable.

    Returns:
        dict: The PORT_CONTEXT as a dictionary, or None if the environment variable is not set or invalid.
    """
    try:
        port_context_raw = os.environ.get('PORT_CONTEXT', None)
        if not port_context_raw:
            logging.error("PORT_CONTEXT environment variable is not set or empty.")
            return None

        logging.info(f"Raw PORT_CONTEXT: {port_context_raw}")

        # Sanitize the malformed JSON
        sanitized_port_context = sanitize_to_json(port_context_raw)
        logging.info(f"Sanitized PORT_CONTEXT: {sanitized_port_context}")

        # Parse JSON
        parsed_port_context = json.loads(sanitized_port_context)
        logging.info(f"PORT_CONTEXT type before returning: {type(parsed_port_context)}")
        return parsed_port_context
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON format in PORT_CONTEXT: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
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