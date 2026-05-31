# Natural Language File Renamer (nlrename)

A CLI tool to batch-rename files using natural language commands.

## Features
- **Natural Language Parsing**: Rename files using commands like `"today's date + original name"`, `"lowercase"`, or `"replace 'old' with 'new'"`.
- **Dry-Run Mode**: Preview changes before applying them.
- **Verbose Output**: See exactly what will be renamed.

## Installation
```bash
pip install click python-dateutil
```

## Usage
```bash
# Dry-run: Preview changes
nlrename "today's date + original name" --dry-run --verbose

# Apply changes
nlrename "lowercase"

# Replace text
nlrename "replace 'old' with 'new'"

# Add prefix/suffix
nlrename "add prefix 'backup_'"
nlrename "add suffix '_backup'"
```

## Examples
| Command                          | Before          | After                |
|---------------------------------|-----------------|----------------------|
| `"today's date + original name"` | `myfile.txt`    | `2026-05-31_myfile.txt` |
| `"lowercase"`                   | `MYFILE.TXT`    | `myfile.txt`          |
| `"replace 'old' with 'new'"`    | `oldfile.txt`   | `newfile.txt`         |
| `"add prefix 'backup_'"`        | `myfile.txt`    | `backup_myfile.txt`   |

## Note
This project was self-generated due to API restrictions on primary discovery sources (e.g., Reddit). No open-source Python CLI tool existed for natural language file renaming at the time of development.

## License
MIT