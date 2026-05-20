import os
import sys
import glob
from datetime import datetime

# Parse .env file (if exists)
env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
if os.path.exists(env_file):
    with open(env_file, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, _, value = line.partition('=')
                os.environ.setdefault(key.strip(), value.strip())

# Config: command-line args take priority over .env
TARGET_FOLDER = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('TARGET_FOLDER', '')
FILE_PATTERN = sys.argv[2] if len(sys.argv) > 2 else os.environ.get('FILE_PATTERN', '*.py')
CODE_BLOCK_TAG = sys.argv[3] if len(sys.argv) > 3 else os.environ.get('CODE_BLOCK_TAG', 'python')

if not TARGET_FOLDER:
    print('Error: TARGET_FOLDER is required. Set in .env or pass as first argument.')
    sys.exit(1)

if not os.path.isdir(TARGET_FOLDER):
    print(f'Error: folder not found: {TARGET_FOLDER}')
    sys.exit(1)

# Collect all matching files (recursive)
pattern = os.path.join(TARGET_FOLDER, '**', FILE_PATTERN)
files = sorted(glob.glob(pattern, recursive=True))

# Build output content
lines = []
for fp in files:
    rel = os.path.relpath(fp, TARGET_FOLDER).replace('\\', '/')
    with open(fp, encoding='utf-8') as f:
        content = f.read()
    lines.append(f'## ./{rel}')
    lines.append('')
    lines.append(f'```{CODE_BLOCK_TAG}')
    lines.append(content.rstrip('\n'))
    lines.append('```')
    lines.append('')

output_content = '\n'.join(lines)

# Write output
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

folder_name = os.path.basename(os.path.normpath(TARGET_FOLDER))
time_str = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = os.path.join(output_dir, f'{folder_name}-{time_str}.md')

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(output_content)

print(f'Done: {len(files)} files -> {output_file}')
