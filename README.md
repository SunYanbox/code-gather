# CodeGather

**CodeGather** is a lightweight Python utility that scans a target folder recursively, collects all matching source files, and consolidates them into a single Markdown document for easy sharing, review, or LLM consumption.

## Features

- **GUI mode** — Folder picker dialog, scrollable preview, copy-to-clipboard, and file export
- **CLI mode** — Headless operation for scripts and automation
- Recursively scan any folder for files matching a given pattern
- Output a clean Markdown document with relative paths as headings
- Configurable code block language tag per file type
- Configuration via `.env` file or command-line arguments
- Timestamped output files for version tracking

## Usage

### GUI Mode (default)

Simply run without arguments to open the interactive window:

```bash
python main.py
```

In the GUI:

1. Click **选择文件夹** (Select Folder) to pick a target directory
2. The scan runs automatically and displays results in a scrollable, selectable preview
3. Use **📋 复制到剪贴板** to copy all content at once
4. Use **💾 保存到 output** to save as a Markdown file to the `output/` directory

If `TARGET_FOLDER` is set in `.env`, the GUI will auto-scan that folder on startup.

### CLI Mode

Pass a folder path as the first argument to run in command-line mode:

```bash
python main.py /path/to/target/folder --pattern "*.py" --tag python
```

Options:

| Argument       | Description                                           | Default                |
|----------------|-------------------------------------------------------|------------------------|
| `path`         | Target folder to scan                                 | (env `TARGET_FOLDER`)  |
| `--pattern`    | Glob pattern for matching files                       | `*.py`                 |
| `--tag`        | Language tag for Markdown code blocks                 | `python`               |
| `--gui`        | Force GUI mode even if a path is provided             | —                      |

### Using .env

Create a `.env` file in the project root (see `.env.example`):

```env
TARGET_FOLDER=/path/to/target/folder
FILE_PATTERN=*.py
CODE_BLOCK_TAG=python
```

### Run Script (Windows)

```
run.cmd
```

Without arguments, this opens the GUI. To use CLI instead, edit the script or pass arguments directly.

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
