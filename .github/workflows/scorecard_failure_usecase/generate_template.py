"""Generate template content by replacing placeholders."""

import os
import sys
from pathlib import Path

# Add scorecard_failure_usecase to path
sys.path.insert(0, str(Path(__file__).parent))

from json_utils import parse_json_with_repair, write_github_output


def extract_entity_title(entity_json_raw: str, fallback_id: str = '') -> str:
    """
    Extract entity title from JSON.
    
    Args:
        entity_json_raw: Raw JSON string from Port GitHub Action
        fallback_id: Fallback identifier if title cannot be extracted
        
    Returns:
        Entity title or identifier
    """
    if not entity_json_raw or entity_json_raw == "null":
        return fallback_id
    
    try:
        entity = parse_json_with_repair(entity_json_raw, "Generate template - entity parsing")
        entity_title = entity.get('title') or entity.get('identifier', fallback_id)
        print(f"Extracted entity title: {entity_title}", file=sys.stderr)
        return entity_title
    except SystemExit:
        print(f"Falling back to entity_id: {fallback_id}", file=sys.stderr)
        return fallback_id


def generate_template_content(
    template: str,
    rule_name: str,
    entity_name: str,
    description: str
) -> str:
    """
    Generate template content by replacing placeholders.
    
    Args:
        template: Template string with placeholders
        rule_name: Rule name to replace {{ Rule }}
        entity_name: Entity name to replace {{ s3 }}
        description: Description to replace {{ Description }}
        
    Returns:
        Generated content with placeholders replaced
    """
    result = template.replace('{{ Rule }}', rule_name)
    result = result.replace('{{ s3 }}', entity_name)
    result = result.replace('{{ Description }}', description)
    return result


def main():
    """Main entry point for template generation script."""
    entity_json_raw = os.environ.get('ENTITY_JSON', '')
    rule_title = os.environ.get('RULE_TITLE', '')
    rule_identifier = os.environ.get('RULE_IDENTIFIER', '')
    rule_description = os.environ.get('RULE_DESCRIPTION', '')
    rule_template = os.environ.get('RULE_TEMPLATE', '')
    entity_id = os.environ.get('ENTITY_ID', '')
    
    # Extract entity title
    entity_title = extract_entity_title(entity_json_raw, entity_id)
    
    # Determine rule display name
    rule_display_name = rule_title if rule_title else rule_identifier
    print(f"Using rule display name: {rule_display_name}", file=sys.stderr)
    print(f"Rule description length: {len(rule_description)} characters", file=sys.stderr)
    print(f"Rule template length: {len(rule_template)} characters", file=sys.stderr)
    
    # Generate template content
    generated_content = generate_template_content(
        rule_template,
        rule_display_name,
        entity_title,
        rule_description
    )
    
    print("Generated template content:")
    print(generated_content)
    print(f"Generated content length: {len(generated_content)} characters", file=sys.stderr)
    
    # Write output
    output_file = os.environ.get('GITHUB_OUTPUT', '/dev/stdout')
    write_github_output('content', generated_content, output_file)


if __name__ == '__main__':
    main()

