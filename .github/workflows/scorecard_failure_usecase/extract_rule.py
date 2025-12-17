"""Extract and validate rule properties from Port entity JSON."""

import os
import sys
from pathlib import Path
from typing import Tuple

# Add scorecard_failure_usecase to path
sys.path.insert(0, str(Path(__file__).parent))

from json_utils import parse_json_with_repair, write_github_output


def extract_rule_properties(entity_json_raw: str) -> dict:
    """
    Extract rule properties from entity JSON and validate required fields.
    
    Args:
        entity_json_raw: Raw JSON string from Port GitHub Action
        
    Returns:
        Dictionary with extracted properties and validation status
    """
    entity = parse_json_with_repair(entity_json_raw, "Extract rule properties")
    
    print("Extracting properties from parsed entity...", file=sys.stderr)
    properties = entity.get('properties', {})
    
    result = {
        'rule_description': properties.get('description', ''),
        'rule_template': properties.get('template', ''),
        'rule_team': entity.get('team', ''),
        'rule_title': entity.get('title') or entity.get('identifier', ''),
        'rule_identifier': entity.get('identifier', ''),
    }
    
    print(f"Extracted values:", file=sys.stderr)
    for key, value in result.items():
        if isinstance(value, str):
            print(f"  - {key}: {value[:50] if len(value) > 50 else value} ({len(value)} chars)", file=sys.stderr)
        else:
            print(f"  - {key}: {value}", file=sys.stderr)
    
    return result


def validate_rule_properties(properties: dict) -> Tuple[bool, str]:
    """
    Validate that required rule properties are present.
    
    Args:
        properties: Dictionary of extracted rule properties
        
    Returns:
        Tuple of (validation_failed: bool, error_message: str)
    """
    rule_identifier = properties['rule_identifier']
    
    if not properties['rule_description'] or properties['rule_description'] == "null":
        error_msg = f"Rule description is missing or null for rule: {rule_identifier}"
        print(f"✗ Validation failed: {error_msg}", file=sys.stderr)
        return True, error_msg
    
    if not properties['rule_template'] or properties['rule_template'] == "null":
        error_msg = f"Rule template is missing or null for rule: {rule_identifier}"
        print(f"✗ Validation failed: {error_msg}", file=sys.stderr)
        return True, error_msg
    
    print("✓ Validation passed: description and template are present", file=sys.stderr)
    return False, ""


def main():
    """Main entry point for rule extraction script."""
    entity_json_raw = os.environ.get('RULE_ENTITY_JSON', '')
    
    if not entity_json_raw:
        print("Error: RULE_ENTITY_JSON environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    properties = extract_rule_properties(entity_json_raw)
    validation_failed, error_message = validate_rule_properties(properties)
    
    output_file = os.environ.get('GITHUB_OUTPUT', '/dev/stdout')
    
    # Write validation status
    write_github_output('VALIDATION_FAILED', str(validation_failed).lower(), output_file)
    
    if validation_failed:
        write_github_output('ERROR_MESSAGE', error_message, output_file)
        sys.exit(0)
    
    # Write extracted properties
    write_github_output('description', properties['rule_description'], output_file)
    write_github_output('template', properties['rule_template'], output_file)
    write_github_output('team', str(properties['rule_team']), output_file)
    write_github_output('title', properties['rule_title'], output_file)
    write_github_output('identifier', properties['rule_identifier'], output_file)
    
    # Print summary
    print(f"Rule Description: {properties['rule_description']}")
    print(f"Rule Template: {properties['rule_template']}")
    print(f"Rule Team: {properties['rule_team']}")


if __name__ == '__main__':
    main()

