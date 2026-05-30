# Natural Language File Renamer (`nlrename`)

Rename files using natural language expressions.

## Features
- **Date transformations**: `"today's date + original name"` → `2026-05-30_original.txt`
- **Case transformations**: `"lowercase"` → `original.txt`, `"uppercase"` → `ORIGINAL.TXT`
- **Replace transformations**: `replace "foo" with "bar"` → `bar.txt`

## Installation
```bash
pip install click python-dateutil
chmod +x nlrename.py
```

## Usage
```bash
# Dry run
./nlrename.py "today's date + original name" *.txt --dry-run

# Rename files
./nlrename.py "today's date + original name" *.txt
./nlrename.py "lowercase" *.JPG
./nlrename.py 'replace "foo" with "bar"' *.md
```

## Examples
| Expression                     | Before          | After                     |
|-------------------------------|-----------------|---------------------------|
| `"today's date + original"`  | `notes.txt`     | `2026-05-30_notes.txt`    |
| `"lowercase"`               | `IMAGE.JPG`     | `image.jpg`               |
| `"uppercase"`               | `notes.txt`     | `NOTES.TXT`               |
| `replace "draft" with "final"` | `draft.txt` | `final.txt`               |

## License
MIT