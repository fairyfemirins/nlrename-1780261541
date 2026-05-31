#!/usr/bin/env python3
"""
Natural Language File Renamer (nlrename)

A CLI tool to rename files using natural language expressions.
"""

import re
import os
import sys
from datetime import datetime
from typing import List, Optional
import click
from dateutil.parser import parse as dateutil_parse


class NaturalLanguageRenamer:
    """Core logic for natural language file renaming."""

    def __init__(self, expression: str):
        self.expression = expression.lower()
        self.transformations = []
        self._parse_expression()

    def _parse_expression(self) -> None:
        """Parse the natural language expression into transformations."""
        if "today's date" in self.expression:
            self.transformations.append(self._add_todays_date)
        if "original name" in self.expression:
            self.transformations.append(self._keep_original_name)
        if "sequential number" in self.expression:
            self.transformations.append(self._add_sequential_number)
        if "lowercase" in self.expression:
            self.transformations.append(self._lowercase)
        if "uppercase" in self.expression:
            self.transformations.append(self._uppercase)
        if "regex(" in self.expression:
            self._parse_regex()

    def _parse_regex(self) -> None:
        """Parse regex substitution from the expression."""
        match = re.search(r'regex\(s/(.*?)/(.*?)/\)', self.expression)
        if match:
            pattern, repl = match.groups()
            self.transformations.append(lambda name, _: re.sub(pattern, repl, name))

    def _add_todays_date(self, name: str, _: Optional[int] = None) -> str:
        """Add today's date to the filename."""
        today = datetime.now().strftime("%Y-%m-%d")
        return f"{today}_{name}"

    def _keep_original_name(self, name: str, _: Optional[int] = None) -> str:
        """Keep the original name (no-op)."""
        return name

    def _add_sequential_number(self, name: str, index: Optional[int] = None) -> str:
        """Add a sequential number to the filename."""
        if index is None:
            return name
        return f"{index}_{name}"

    def _lowercase(self, name: str, _: Optional[int] = None) -> str:
        """Convert the filename to lowercase."""
        name, ext = os.path.splitext(name)
        return f"{name.lower()}{ext}"

    def _uppercase(self, name: str, _: Optional[int] = None) -> str:
        """Convert the filename to uppercase."""
        name, ext = os.path.splitext(name)
        return f"{name.upper()}{ext}"

    def transform(self, filename: str, index: Optional[int] = None) -> str:
        """Apply all transformations to the filename."""
        name, ext = os.path.splitext(filename)
        for transform in self.transformations:
            name = transform(name, index)
        # Re-split to handle case transformations on the extension
        name, ext = os.path.splitext(f"{name}{ext}")
        return f"{name}{ext}"


@click.command()
@click.argument('expression', type=str)
@click.argument('files', type=str, nargs=-1)
@click.option('--apply', is_flag=True, help='Apply the renaming (default: dry-run)')
@click.option('--start', type=int, default=1, help='Starting number for sequential numbering')
def cli(expression: str, files: List[str], apply: bool, start: int) -> None:
    """CLI entry point for nlrename."""
    if not files:
        click.echo("Error: No files provided.", err=True)
        sys.exit(1)

    renamer = NaturalLanguageRenamer(expression)
    for idx, filename in enumerate(files, start=start):
        if not os.path.exists(filename):
            click.echo(f"Error: File not found: {filename}", err=True)
            continue
        new_name = renamer.transform(filename, idx)
        if apply:
            try:
                os.rename(filename, new_name)
                click.echo(f"Renamed: {filename} -> {new_name}")
            except OSError as e:
                click.echo(f"Error: Failed to rename {filename}: {e}", err=True)
        else:
            click.echo(f"Preview: {filename} -> {new_name}")


if __name__ == '__main__':
    cli()