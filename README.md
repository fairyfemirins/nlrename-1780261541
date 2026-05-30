# Natural Language File Renamer (`nlrename`)

A CLI tool to rename files using **natural language patterns** (e.g., `"today's date + original name"`).

## Features
- **Natural Language Parsing**: Use patterns like `"today's date + original name"`, `"lowercase"`, or `"replace foo with bar"`.
- **Dry Run Mode**: Preview changes before applying them.
- **Cross-Platform**: Works on Linux, macOS, and Windows.

## Installation
```bash
pip install nlrename
```

## Usage
```bash
# Dry run (preview changes)
nlrename file.txt -p "today's date + original name" --dry-run

# Rename for real
nlrename file.txt -p "today's date + original name"

# Batch rename
nlrename *.txt -p "lowercase"
```

## Supported Patterns
| Pattern                     | Example Output               |
|-----------------------------|------------------------------|
| `today's date + original`   | `2026-05-30 + file.txt`      |
| `tomorrow + original`       | `2026-05-31 + file.txt`      |
| `next monday + original`    | `2026-06-02 + file.txt`      |
| `lowercase`                 | `file.txt` → `file.txt`      |
| `uppercase`                 | `file.txt` → `FILE.TXT`      |
| `replace "foo" with "bar"` | `foobar.txt` → `barbar.txt`  |

## Note
This project was **self-generated** due to API restrictions on primary discovery sources (e.g., Reddit).

## License
MIT