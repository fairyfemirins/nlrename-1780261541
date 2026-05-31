# Natural Language File Renamer (nlrename)

A Python CLI tool to rename files using natural language expressions (e.g., `"today's date + original name"`, `"lowercase + sequential number"`).

## Why?
- **No open-source Python CLI tool** exists for natural language file renaming.
- **Regex-based tools** (e.g., `F2`, `nom`) require users to learn regex syntax.
- **AI-powered tools** (e.g., `renaiming`) suggest names but do not support natural language expressions as input.

## Features
- Rename files using natural language expressions:
  - `"today's date + original name"` → `2026-05-31_original_name.txt`
  - `"lowercase + sequential number"` → `file_1.txt`, `file_2.txt`
  - `"uppercase + regex(s/foo/bar/)"` → `BAR.txt`
- Preview changes before applying them.
- Dry-run mode to test transformations.

## Limitations
- **Self-Generated Project**: This project was self-generated due to API restrictions on primary discovery sources (e.g., Reddit).
- **Cron Mode Publishing**: Published under a timestamped repository name due to namespace restrictions. See [TRANSFER.md](TRANSFER.md) for transfer instructions.

## Installation
```bash
pip install nlrename
```

## Usage
```bash
# Preview changes (dry-run)
nlrename "today's date + original name" *.txt

# Apply changes
nlrename --apply "today's date + original name" *.txt

# Sequential numbering
nlrename "sequential number + original name" *.jpg

# Regex substitution
nlrename "regex(s/foo/bar/)" *.txt

# Lowercase
nlrename "lowercase" *.TXT
```

## Examples
| Expression                     | Before          | After                |
|-------------------------------|-----------------|----------------------|
| `"today's date + original name"` | `notes.txt`     | `2026-05-31_notes.txt` |
| `"sequential number + original name"` | `photo.jpg` | `1_photo.jpg`        |
| `"regex(s/foo/bar/)"`        | `foo.txt`       | `bar.txt`            |
| `"lowercase"`                | `FILE.TXT`      | `file.txt`           |

## Development
```bash
# Clone the repository
git clone https://github.com/fairyfemirins/nlrename-$(date +%s).git
cd nlrename

# Install dependencies
pip install -e .

# Run tests
pytest
```

## License
MIT