"""JSON parsing utilities for GitHub Actions workflow."""

import json
import sys
from typing import Dict, Any, Tuple, Optional


def repair_json(json_str: str) -> Tuple[str, int]:
    """
    Repair JSON string by escaping control characters within string values.
    
    Args:
        json_str: Raw JSON string that may contain unescaped control characters
        
    Returns:
        Tuple of (repaired_json_string, number_of_characters_fixed)
    """
    result = []
    chars_fixed = 0
    in_string = False
    escape_next = False
    
    for char in json_str:
        if escape_next:
            result.append(char)
            escape_next = False
            continue
            
        if char == '\\':
            result.append(char)
            escape_next = True
            continue
            
        if char == '"' and not escape_next:
            in_string = not in_string
            result.append(char)
            continue
            
        if not in_string:
            result.append(char)
            continue
        
        # Handle control characters within strings
        control_chars = {
            '\n': '\\n',
            '\r': '\\r',
            '\t': '\\t'
        }
        
        if char in control_chars:
            result.append(control_chars[char])
            chars_fixed += 1
        else:
            result.append(char)
    
    return ''.join(result), chars_fixed


def parse_json_with_repair(json_str: str, step_name: str = "Unknown") -> Dict[str, Any]:
    """
    Parse JSON string, attempting repair if initial parse fails.
    
    Args:
        json_str: Raw JSON string to parse
        step_name: Name of the step for logging purposes
        
    Returns:
        Parsed JSON as dictionary
        
    Raises:
        SystemExit: If JSON cannot be parsed even after repair
    """
    if not json_str or json_str.strip() == "null":
        print(f"Error: {step_name} - JSON string is empty or null", file=sys.stderr)
        sys.exit(1)
    
    print(f"Step: {step_name} - Starting JSON parsing", file=sys.stderr)
    print(f"JSON length: {len(json_str)} characters", file=sys.stderr)
    print(f"JSON preview (first 200 chars): {json_str[:200]}", file=sys.stderr)
    
    # Try initial parse
    try:
        print("Attempting initial JSON parse...", file=sys.stderr)
        entity = json.loads(json_str)
        print("✓ Initial JSON parse succeeded", file=sys.stderr)
        return entity
    except json.JSONDecodeError as initial_error:
        print(f"✗ Initial JSON parse failed: {initial_error}", file=sys.stderr)
        error_pos = getattr(initial_error, 'pos', 'unknown')
        print(f"Error at position: {error_pos}", file=sys.stderr)
    
    # Attempt repair
    print("Attempting JSON repair (escaping control characters)...", file=sys.stderr)
    fixed_json, chars_fixed = repair_json(json_str)
    print(f"JSON repair complete: fixed {chars_fixed} control characters", file=sys.stderr)
    print(f"Fixed JSON preview (first 200 chars): {fixed_json[:200]}", file=sys.stderr)
    
    # Try parsing repaired JSON
    try:
        entity = json.loads(fixed_json)
        print("✓ JSON parse succeeded after repair", file=sys.stderr)
        return entity
    except json.JSONDecodeError as repair_error:
        print(f"✗ JSON parse failed after repair: {repair_error}", file=sys.stderr)
        error_pos = getattr(repair_error, 'pos', 'unknown')
        error_msg = getattr(repair_error, 'msg', 'unknown error')
        print(f"Error at position: {error_pos}", file=sys.stderr)
        print(f"Error message: {error_msg}", file=sys.stderr)
        print(f"Raw JSON (first 1000 chars): {json_str[:1000]}", file=sys.stderr)
        print(f"Fixed JSON (first 1000 chars): {fixed_json[:1000]}", file=sys.stderr)
        sys.exit(1)


def write_github_output(key: str, value: str, output_file: str) -> None:
    """
    Write GitHub Actions output, using multiline format if value contains newlines.
    
    Args:
        key: Output key name
        value: Output value
        output_file: Path to GitHub Actions output file
    """
    with open(output_file, 'a') as f:
        if '\n' in value:
            f.write(f"{key}<<EOF\n{value}\nEOF\n")
        else:
            f.write(f"{key}={value}\n")

