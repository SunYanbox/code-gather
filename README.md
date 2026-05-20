# CodeGather

**CodeGather** is a lightweight Python utility that scans a target folder recursively, collects all matching source files, and consolidates them into a single Markdown document for easy sharing, review, or LLM consumption.

## Features

- Recursively scan any folder for files matching a given pattern
- Output a clean Markdown document with relative paths as headings
- Configurable code block language tag per file type
- Configuration via `.env` file or command-line arguments
- Timestamped output files for version tracking

## Usage

### Command Line

```bash
python main.py /path/to/target/folder "*.py" python
```

Arguments (in order):
1. `TARGET_FOLDER` — Path to the folder to scan (required)
2. `FILE_PATTERN` — Glob pattern for matching files (optional, default: `*.py`)
3. `CODE_BLOCK_TAG` — Language tag for Markdown code blocks (optional, default: `python`)

### Using .env

Create a `.env` file in the project root (see `.env.example`):

```env
TARGET_FOLDER=/path/to/target/folder
FILE_PATTERN=*.py
CODE_BLOCK_TAG=python
```

Then simply run:

```bash
python main.py
```

### Run Script (Windows)

```
run.cmd
```

## Output

Generated files are saved in the `output/` directory with the format:

```
output/{folder_name}-{YYYYMMDD_HHMMSS}.md
```

Each source file is formatted as:

```markdown
## ./relative/path/to/file.py

\`\`\`python
file content here
\`\`\`
```

## Requirements

- Python 3.12+
- No third-party dependencies required

## License

MIT
