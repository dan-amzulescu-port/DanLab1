import json
import logging
import os
from datetime import datetime, timedelta
import pytz

def get_port_context():
    """
    Retrieves the PORT_CONTEXT from the environment variable.

    Returns:
        The PORT_CONTEXT as a dictionary, or None if the environment variable is not set or invalid.
    """
    try:
        port_context = os.environ['PORT_CONTEXT']  # Get the JSON string from the environment
        logging.info(f"PORT_CONTEXT loaded: {port_context}")
        return json.loads(port_context)  # Parse the JSON string
    except KeyError:
        logging.error("PORT_CONTEXT environment variable is not set.")
        return None
    except json.JSONDecodeError:
        logging.error("Invalid JSON format in PORT_CONTEXT.")
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