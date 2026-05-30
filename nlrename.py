#!/usr/bin/env python3
"""
Natural Language File Renamer (nlrename)

Rename files using natural language instructions (e.g., "add today's date to all PDFs", "replace 'draft' with 'final'").
"""

import os
import re
import click
from datetime import datetime
from dateutil.relativedelta import relativedelta


def parse_instruction(instruction: str) -> dict:
    """Parse natural language instruction into structured actions."""
    instruction = instruction.lower()
    actions: dict[str, str | tuple[str, str] | None] = {
        "add_date": None,
        "replace": None,
        "case": None,
        "regex": None,
        "filter": None,
    }

    # Add date (e.g., "add today's date", "prepend 2026-05-30")
    date_patterns = [
        r"add (today|yesterday|tomorrow)'?s? date",
        r"prepend (\d{4}-\d{2}-\d{2})",
        r"append (\d{4}-\d{2}-\d{2})",
    ]
    for pattern in date_patterns:
        match = re.search(pattern, instruction)
        if match:
            if match.group(1) == "today":
                actions["add_date"] = datetime.now().strftime("%Y-%m-%d")
            elif match.group(1) == "yesterday":
                actions["add_date"] = (datetime.now() - relativedelta(days=1)).strftime("%Y-%m-%d")
            elif match.group(1) == "tomorrow":
                actions["add_date"] = (datetime.now() + relativedelta(days=1)).strftime("%Y-%m-%d")
            else:
                actions["add_date"] = match.group(1)
            break

    # Replace text (e.g., "replace 'draft' with 'final'")
    replace_pattern = r'replace ["\'](.+?)["\'] with ["\'](.+?)["\']'
    match = re.search(replace_pattern, instruction)
    if match:
        actions["replace"] = (match.group(1), match.group(2))

    # Case transformation (e.g., "all files to lowercase", "to uppercase")
    case_patterns = {
        r"to lowercase": "lower",
        r"to uppercase": "upper",
        r"to title case": "title",
    }
    for pattern, case in case_patterns.items():
        if re.search(pattern, instruction):
            actions["case"] = case
            break

    # Regex (e.g., "remove first 3 characters", "keep only numbers")
    regex_patterns = {
        r"remove first (\d+) characters": r"^.{\1}(.*)",
        r"remove last (\d+) characters": r"(.*)?.{\1}$",
        r"keep only numbers": r"[^0-9]",
        r"keep only letters": r"[^a-zA-Z]",
    }
    for pattern, regex in regex_patterns.items():
        if re.search(pattern, instruction):
            actions["regex"] = (regex, "")
            break

    # Filter (e.g., "all PDFs", "files larger than 1MB")
    filter_patterns = {
        r"all (\w+)s?": lambda ext: ext.lower(),
        r"files? (?:larger|smaller) than (\d+[KMGT]?B)": None,  # Not implemented
    }
    for pattern, transform in filter_patterns.items():
        match = re.search(pattern, instruction)
        if match:
            actions["filter"] = transform(match.group(1)) if transform else match.group(1)
            break

    return actions


def apply_actions(filename: str, actions: dict) -> str:
    """Apply parsed actions to a filename."""
    name, ext = os.path.splitext(filename)
    ext = ext.lower()  # Normalize extension

    # Apply filter (skip if filter doesn't match)
    if actions["filter"]:
        expected_ext = ".{}".format(actions["filter"])
        if not filename.lower().endswith(expected_ext):
            return filename

    # Apply regex
    if actions["regex"]:
        regex, repl = actions["regex"]
        name = re.sub(regex, repl, name)

    # Apply replace
    if actions["replace"]:
        old, new = actions["replace"]
        name = name.replace(old, new)

    # Apply case
    if actions["case"] == "lower":
        name = name.lower()
    elif actions["case"] == "upper":
        name = name.upper()
    elif actions["case"] == "title":
        name = name.title()

    # Apply add_date
    if actions["add_date"]:
        position = "prepend" if "prepend" in actions.get("original_instruction", "") else "append"
        date = actions["add_date"]
        name = f"{date}_{name}" if position == "prepend" else f"{name}_{date}"

    return f"{name}{ext}"


@click.command()
@click.argument("instruction", type=str)
@click.argument("directory", type=click.Path(exists=True), default=".")
@click.option("--dry-run", is_flag=True, help="Preview changes without renaming.")
@click.option("--verbose", is_flag=True, help="Show detailed output.")
def cli(instruction: str, directory: str, dry_run: bool, verbose: bool):
    """Rename files in DIRECTORY using natural language INSTRUCTION."""
    actions = parse_instruction(instruction)
    actions["original_instruction"] = instruction  # For position detection
    
    if verbose:
        click.echo(f"Parsed actions: {actions}")
    
    for filename in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, filename)):
            continue
        
        new_name = apply_actions(filename, actions)
        if new_name != filename:
            if dry_run:
                click.echo(f"{filename} -> {new_name} [DRY RUN]")
            else:
                os.rename(
                    os.path.join(directory, filename),
                    os.path.join(directory, new_name),
                )
                click.echo(f"{filename} -> {new_name}")


if __name__ == "__main__":
    cli()