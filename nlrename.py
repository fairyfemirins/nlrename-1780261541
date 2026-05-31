#!/usr/bin/env python3
"""
Natural Language File Renamer (nlrename)

A CLI tool to batch-rename files using natural language commands.
Example: "today's date + original name" -> "2026-05-31_myfile.txt"

Usage:
  nlrename "<natural-language-command>" [--dry-run] [--verbose]

Commands:
  - "today's date + original name" -> "2026-05-31_myfile.txt"
  - "lowercase" -> "myfile.txt"
  - "uppercase" -> "MYFILE.TXT"
  - "replace 'old' with 'new'" -> "newfile.txt"
  - "add prefix 'backup_'" -> "backup_myfile.txt"
  - "add suffix '_backup'" -> "myfile_backup.txt"

Dependencies:
  - click
  - python-dateutil
"""

import os
import re
import sys
from datetime import datetime
from typing import List, Optional

import click
from dateutil.relativedelta import relativedelta


class NaturalLanguageParser:
    """Parse natural language commands into renaming rules."""

    @staticmethod
    def parse(command: str) -> dict:
        """Parse a natural language command into a renaming rule."""
        command = command.lower().strip()
        rule = {"transformations": []}

        # Date-based transformations
        if "today's date" in command:
            today = datetime.now().strftime("%Y-%m-%d")
            if "+" in command:
                rule["transformations"].append({"type": "prefix", "value": f"{today}_"})
            else:
                rule["transformations"].append({"type": "suffix", "value": f"_{today}"})

        # Case transformations
        if "lowercase" in command:
            rule["transformations"].append({"type": "lowercase"})
        elif "uppercase" in command:
            rule["transformations"].append({"type": "uppercase"})

        # Replace transformations
        replace_match = re.search(r"replace ['\"](.*?)['\"] with ['\"](.*?)['\"]", command)
        if replace_match:
            rule["transformations"].append({
                "type": "replace",
                "old": replace_match.group(1),
                "new": replace_match.group(2),
            })

        # Prefix/suffix transformations
        prefix_match = re.search(r"add prefix ['\"](.*?)['\"]", command)
        if prefix_match:
            rule["transformations"].append({"type": "prefix", "value": prefix_match.group(1)})

        suffix_match = re.search(r"add suffix ['\"](.*?)['\"]", command)
        if suffix_match:
            rule["transformations"].append({"type": "suffix", "value": suffix_match.group(1)})

        return rule

    @staticmethod
    def apply_transformations(filename: str, rule: dict) -> str:
        """Apply transformations to a filename."""
        for transform in rule["transformations"]:
            if transform["type"] == "prefix":
                filename = transform["value"] + filename
            elif transform["type"] == "suffix":
                filename = filename + transform["value"]
            elif transform["type"] == "lowercase":
                filename = filename.lower()
            elif transform["type"] == "uppercase":
                filename = filename.upper()
            elif transform["type"] == "replace":
                filename = filename.replace(transform["old"], transform["new"])
        return filename


@click.command()
@click.argument("command", type=str)
@click.option("--dry-run", is_flag=True, help="Show what would be renamed without making changes.")
@click.option("--verbose", is_flag=True, help="Show detailed output.")
def cli(command: str, dry_run: bool, verbose: bool) -> None:
    """Rename files using natural language commands."""
    parser = NaturalLanguageParser()
    rule = parser.parse(command)
    
    if not rule["transformations"]:
        click.echo("Error: Could not parse the command. Example: 'today's date + original name'")
        sys.exit(1)
    
    for filename in os.listdir("."):
        if os.path.isfile(filename):
            new_name = parser.apply_transformations(filename, rule)
            if new_name != filename:
                if verbose:
                    click.echo(f"Renaming: {filename} -> {new_name}")
                if not dry_run:
                    os.rename(filename, new_name)
    
    if dry_run:
        click.echo("Dry run complete. No files were renamed.")


if __name__ == "__main__":
    cli()