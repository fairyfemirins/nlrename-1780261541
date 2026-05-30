import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

def parse_natural_language(pattern: str, original_name: str) -> str:
    """
    Parse natural language patterns like:
    - "today's date + original name"
    - "next monday + original name"
    - "lowercase"
    - "uppercase"
    - "replace foo with bar"
    """
    today = datetime.now()
    
    # Date patterns
    if "today" in pattern:
        date_str = today.strftime("%Y-%m-%d")
        pattern = pattern.replace("today's date", date_str)
    if "tomorrow" in pattern:
        tomorrow = today + relativedelta(days=1)
        date_str = tomorrow.strftime("%Y-%m-%d")
        pattern = pattern.replace("tomorrow", date_str)
    if "next monday" in pattern:
        next_monday = today + relativedelta(days=(0 - today.weekday()) % 7 + 7)
        date_str = next_monday.strftime("%Y-%m-%d")
        pattern = pattern.replace("next monday", date_str)
    
    # Case transformations
    if "lowercase" in pattern:
        original_name = original_name.lower()
        pattern = pattern.replace("lowercase", "").strip()
    if "uppercase" in pattern:
        original_name = original_name.upper()
        pattern = pattern.replace("uppercase", "").strip()
    
    # Replace patterns
    if "replace" in pattern:
        match = re.search(r'replace "(.+?)" with "(.+?)"', pattern)
        if match:
            old, new = match.groups()
            original_name = original_name.replace(old, new)
            pattern = pattern.replace(f'replace "{old}" with "{new}"', "").strip()
    
    # Combine with original name
    if "original name" in pattern:
        pattern = pattern.replace("original name", original_name)
    else:
        pattern = f"{pattern} {original_name}".strip()
    
    return pattern