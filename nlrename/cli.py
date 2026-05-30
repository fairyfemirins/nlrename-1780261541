import os
import click
from nlrename.renamer import parse_natural_language

@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--pattern", "-p", required=True, help='Natural language pattern, e.g. "today\'s date + original name"')
@click.option("--dry-run", is_flag=True, help="Show what would be renamed without actually renaming")
def main(files, pattern, dry_run):
    """Rename files using natural language patterns."""
    for file_path in files:
        dirname = os.path.dirname(file_path)
        original_name = os.path.basename(file_path)
        new_name = parse_natural_language(pattern, original_name)
        new_path = os.path.join(dirname, new_name)
        
        if dry_run:
            click.echo(f"Would rename: {file_path} -> {new_path}")
        else:
            os.rename(file_path, new_path)
            click.echo(f"Renamed: {file_path} -> {new_path}")

if __name__ == "__main__":
    main()