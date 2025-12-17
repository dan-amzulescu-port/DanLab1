"""Create scorecard task entity with properties and relations."""

import json
import os
import sys
from pathlib import Path

# Add scorecard_failure_usecase to path
sys.path.insert(0, str(Path(__file__).parent))

from json_utils import parse_json_with_repair


def extract_team_identifier(team_value: str) -> str:
    """
    Extract team identifier from value (handles both array and string).
    
    Args:
        team_value: Team value that may be JSON array, string, or empty
        
    Returns:
        Team identifier string or empty string
    """
    if not team_value or team_value == "null":
        return ""
    
    try:
        parsed = json.loads(team_value)
        if isinstance(parsed, list) and len(parsed) > 0:
            return str(parsed[0])
        if parsed:
            return str(parsed)
        return ""
    except (json.JSONDecodeError, TypeError):
        return team_value if team_value else ""


def extract_entity_title_for_task(entity_json_raw: str, fallback_id: str) -> str:
    """
    Extract entity title for task creation (with fallback handling).
    
    Args:
        entity_json_raw: Raw JSON string from Port GitHub Action
        fallback_id: Fallback identifier if parsing fails
        
    Returns:
        Entity title or identifier
    """
    if not entity_json_raw or entity_json_raw == "null":
        print(f"Entity JSON is empty or null, using fallback: {fallback_id}", file=sys.stderr)
        return fallback_id
    
    try:
        entity = parse_json_with_repair(entity_json_raw, "Create task - entity parsing")
        entity_title = entity.get('title') or entity.get('identifier', fallback_id)
        print(f"✓ Entity title extracted: {entity_title}", file=sys.stderr)
        return entity_title
    except SystemExit:
        print(f"✗ Entity parsing failed, falling back to: {fallback_id}", file=sys.stderr)
        return fallback_id


def create_task_title(rule_title: str, rule_identifier: str, entity_title: str) -> str:
    """
    Create task title from rule and entity information.
    
    Args:
        rule_title: Rule title (may be empty)
        rule_identifier: Rule identifier (fallback)
        entity_title: Entity title
        
    Returns:
        Formatted task title
    """
    rule_display = rule_title if rule_title else rule_identifier
    return f"Task: {rule_display} - {entity_title}"


def create_properties_json(resolution_content: str) -> str:
    """
    Create properties JSON for the task entity.
    
    Args:
        resolution_content: Generated resolution markdown content
        
    Returns:
        JSON string with properties
    """
    properties = {'resolution': resolution_content}
    return json.dumps(properties)


def create_relations_json(rule_id: str, entity_id: str, team_id: str) -> str:
    """
    Create relations JSON for the task entity.
    
    Args:
        rule_id: Rule entity identifier
        entity_id: Entity identifier (s3)
        team_id: Team identifier (optional)
        
    Returns:
        JSON string with relations
    """
    relations = {
        'rule': rule_id,
        's_3': entity_id
    }
    
    if team_id and team_id != "null":
        relations['team'] = team_id
    
    return json.dumps(relations)


def main():
    """Main entry point for task creation script."""
    # Get inputs from environment
    team_value = os.environ.get('TEAM_VALUE', '')
    resolution_content = os.environ.get('RESOLUTION_CONTENT', '')
    rule_title = os.environ.get('RULE_TITLE', '')
    rule_identifier = os.environ.get('RULE_IDENTIFIER', '')
    entity_json_raw = os.environ.get('ENTITY_JSON', '')
    entity_id = os.environ.get('ENTITY_ID', '')
    rule_id = os.environ.get('RULE_ID', '')
    
    # Extract values
    team_identifier = extract_team_identifier(team_value)
    entity_title = extract_entity_title_for_task(entity_json_raw, entity_id)
    task_title = create_task_title(rule_title, rule_identifier, entity_title)
    
    # Create JSON objects
    properties_json = create_properties_json(resolution_content)
    relations_json = create_relations_json(rule_id, entity_id, team_identifier)
    
    # Print summary
    print("Creating scorecard task entity:")
    print(f"  Title: {task_title}")
    print(f"  Rule: {rule_id}")
    print(f"  Entity: {entity_id}")
    print(f"  Team: {team_identifier}")
    print(f"  Properties: {properties_json}")
    print(f"  Relations: {relations_json}")
    
    # Write outputs using multiline format
    output_file = os.environ.get('GITHUB_OUTPUT', '/dev/stdout')
    
    with open(output_file, 'a') as f:
        f.write(f"task_title={task_title}\n")
        f.write(f"properties<<EOF\n{properties_json}\nEOF\n")
        f.write(f"relations<<EOF\n{relations_json}\nEOF\n")


if __name__ == '__main__':
    main()

