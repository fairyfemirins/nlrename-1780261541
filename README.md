# Natural Language File Renamer (nlrename)

Rename files using natural language instructions.

## Features
- **Natural Language Instructions**: Rename files using plain English (e.g., `"add today's date to all PDFs"`, `"replace 'draft' with 'final'"`).
- **Bulk Operations**: Apply changes to all files in a directory.
- **Dry Run Mode**: Preview changes with `--dry-run`.
- **Case Transformation**: Convert filenames to `lowercase`, `UPPERCASE`, or `Title Case`.
- **Regex Support**: Remove first/last N characters, keep only numbers/letters.
- **Filter by Extension**: Rename only specific file types (e.g., `"all PDFs"`).

## Installation
```bash
pip install click python-dateutil regex
```

## Usage
```bash
# Preview changes
./nlrename.py "replace 'draft' with 'final'" /path/to/files --dry-run

# Apply changes
./nlrename.py "add today's date to all PDFs" /path/to/files

# Verbose output
./nlrename.py "to lowercase" /path/to/files --verbose
```

## Examples
| Instruction                          | Before          | After                     |
|-------------------------------------|-----------------|--------------------------|
| `"add today's date to all PDFs"`   | `report.pdf`    | `2026-05-30_report.pdf`   |
| `"replace 'draft' with 'final'"`   | `draft1.txt`    | `final1.txt`             |
| `"to lowercase"`                   | `UPPERCASE.TXT` | `uppercase.txt`          |
| `"remove first 3 characters"`      | `abc123.txt`    | `123.txt`                |
| `"all PDFs to title case"`         | `my report.pdf` | `My Report.pdf`          |

## Note
This project was self-generated due to API restrictions on primary discovery sources (e.g., Reddit).

## License
MIT