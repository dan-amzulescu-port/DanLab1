from datetime import datetime, timedelta
import pytz


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
    current_time = datetime.now(pytz.UTC)

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