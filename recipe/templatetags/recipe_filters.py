from django import template
import re

register = template.Library()

@register.filter
def split(value, arg):
    return [x for x in value.split(arg) if x.strip()]

@register.filter
def strip(value):
    return value.strip()

@register.filter(name='split_lines')
def split_lines(value):
    if value:
        return value.split('\n')
    return []

@register.filter(name='format_steps')
def format_steps(value):
    """
    Handles both list-like and string-like steps.
    - If value is a list or string representation of a list: extracts items inside single quotes.
    - If value is a string with newlines: splits and cleans each line.
    Automatically numbers steps if not already numbered.
    Skips steps that are image URLs or 'Sample image urls:' lines.
    """
    import re
    if not value:
        return []
    # If value is a list, or a string representation of a list
    if isinstance(value, list) or (isinstance(value, str) and value.startswith('[') and value.endswith(']')):
        # Convert to string if it's a list
        if isinstance(value, list):
            value = str(value)
        lines = re.findall(r"'([^']+)'", value)
    else:
        # Otherwise, treat as a newline-separated string
        lines = [line.strip() for line in value.split('\n') if line.strip()]

    formatted_steps = []
    step_number = 1
    skip_rest = False
    for line in lines:
        # If we hit "Sample image urls:", skip this and all following lines
        if re.match(r'^\s*sample\s+image\s+urls\s*:?$', line, re.IGNORECASE):
            skip_rest = True
            continue
        if skip_rest:
            continue
        # Skip if the line is any URL (image or not)
        if re.search(r'https?://', line):
            continue
        # Check if the line already starts with a number (like "1. " or "1) " or similar)
        if not re.match(r'^\d+[\.\)\-]?\s+', line):
            # If not already numbered, add step number
            formatted_step = f"{step_number}. {line}"
            step_number += 1
        else:
            # If it's already numbered, keep as is but ensure consistent formatting
            match = re.match(r'^\d+', line)
            if match:
                try:
                    step_number = int(match.group(0)) + 1
                except ValueError:
                    pass
            formatted_step = line
        formatted_steps.append(formatted_step)
    return formatted_steps


@register.filter(name='format_ingredients')
def format_ingredients(value):
    """
    Handles both list-like and string-like ingredients.
    - If value is a list or string representation of a list: extracts items inside single quotes.
    - If value is a string with newlines: splits and cleans each line.
    """
    import re
    if not value:
        return []
    # If value is a list, or a string representation of a list
    if isinstance(value, list) or (isinstance(value, str) and value.startswith('[') and value.endswith(']')):
        # Convert to string if it's a list
        if isinstance(value, list):
            value = str(value)
        matches = re.findall(r"'([^']+)'", value)
        return [item.strip() for item in matches if item.strip()]
    # Otherwise, treat as a newline-separated string
    lines = [line.strip() for line in value.split('\n') if line.strip()]
    formatted_ingredients = []
    for line in lines:
        clean_line = re.sub(r'^[\-\•\*\★]\s*', '', line).strip()
        formatted_ingredients.append(clean_line)
    return formatted_ingredients