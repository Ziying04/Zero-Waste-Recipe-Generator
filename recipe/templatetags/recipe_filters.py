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
    Format recipe steps by automatically numbering them if they aren't already.
    Also handles formatting and cleaning.
    """
    if not value:
        return []
    
    lines = [line.strip() for line in value.split('\n') if line.strip()]
    formatted_steps = []
    step_number = 1
    
    for line in lines:
        # Check if the line already starts with a number (like "1. " or "1) " or similar)
        if not re.match(r'^\d+[\.\)\-]?\s+', line):
            # If not already numbered, add step number
            formatted_step = f"{step_number}. {line}"
            step_number += 1
        else:
            # If it's already numbered, keep as is but ensure consistent formatting
            # Extract the existing number and adjust our counter
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
    Format ingredients list with consistent bullet points and spacing.
    """
    if not value:
        return []
    
    lines = [line.strip() for line in value.split('\n') if line.strip()]
    formatted_ingredients = []
    
    for line in lines:
        # Remove existing bullet points or dashes
        clean_line = re.sub(r'^[\-\•\*\★]\s*', '', line).strip()
        # Add a consistent bullet point format
        formatted_ingredients.append(clean_line)
    
    return formatted_ingredients

