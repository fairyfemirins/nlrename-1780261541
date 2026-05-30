#!/usr/bin/env python3
"""
nlrename: Rename files using natural language expressions.

Examples:
  nlrename "today's date + original name" *.txt
  nlrename "lowercase" *.JPG
  nlrename "replace foo with bar" *.md
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

import click


@click.command()
@click.argument("expression", type=str)
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--dry-run", is_flag=True, help="Show what would be renamed without actually doing it.")
def cli(expression: str, files: tuple, dry_run: bool) -> None:
    """Rename files using natural language expressions."""
    if not files:
        click.echo("Error: No files provided.", err=True)
        sys.exit(1)

    for file in files:
        original_path = Path(file)
        new_name = parse_expression(expression, original_path.name)
        new_path = original_path.with_name(new_name)

        if dry_run:
            click.echo(f"Would rename: {original_path.name} -> {new_name}")
        else:
            try:
                original_path.rename(new_path)
                click.echo(f"Renamed: {original_path.name} -> {new_name}")
            except Exception as e:
                click.echo(f"Error renaming {original_path.name}: {e}", err=True)


def parse_expression(expression: str, original_name: str) -> str:
    """Parse natural language expression and apply transformations."""
    name, ext = os.path.splitext(original_name)
    result = name

    # Date transformations
    if "today's date" in expression:
        today = datetime.now().strftime("%Y-%m-%d")
        result = f"{today}_{result}"

    # Case transformations
    if "lowercase" in expression:
        result = result.lower()
        ext = ext.lower()
    if "uppercase" in expression:
        result = result.upper()
        ext = ext.upper()
    if "titlecase" in expression:
        result = result.title()

    # Replace transformations
    replace_match = re.search(r'replace "([^"]+)" with "([^"]+)"', expression)
    if replace_match:
        old, new = replace_match.groups()
        result = result.replace(old, new)

    return f"{result}{ext}"


if __name__ == "__main__":
    cli()