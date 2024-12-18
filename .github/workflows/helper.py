import json
import logging
import os
from datetime import datetime, timedelta
import pytz

def get_port_context():
  """
  Retrieves the PORT_CONTEXT from the GITHUB_ENV environment variable.

  Returns:
    The PORT_CONTEXT as a dictionary, or None if the environment variable is not set.
  """
  try:
    with open(os.environ['GITHUB_ENV'], 'r') as f:
      for line in f:
        key, value = line.strip().split('=', 1)
        if key == 'PORT_CONTEXT':
          try:
            logging.info(f"PORT_CONTEXT found: {value}")
            return json.loads(value)
          except json.JSONDecodeError:
            logging.error(f"Error: Invalid JSON for PORT_CONTEXT: {value}")
            return None
  except FileNotFoundError:
    logging.error(f"Error: GITHUB_ENV file not found.")
    return None
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