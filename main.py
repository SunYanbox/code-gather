import os
import re
import sys
import argparse
from datetime import datetime
from pathlib import Path

DEFAULT_EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.idea', '.vscode'}

def load_env(env_path):
    if not env_path.exists():
        return
    with open(env_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # 处理 export KEY=VAL 的情况
            if line.startswith('export '):
                line = line[7:].strip()
            
            key, _, value = line.partition('=')
            if not key:
                continue
            
            key = key.strip()
            value = value.strip()
            # 简单处理引号 (不处理转义字符，如需完善建议用 python-dotenv)
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
                
            os.environ.setdefault(key, value)

# 使用 argparse 替代 sys.argv
def parse_args():
    parser = argparse.ArgumentParser(description='Combine files into a single Markdown file.')
    parser.add_argument('path', nargs='?', default=os.environ.get('TARGET_FOLDER', ''), 
                        help='Target folder to scan (default: env TARGET_FOLDER)')
    parser.add_argument('--pattern', default=os.environ.get('FILE_PATTERN', '*.py'), 
                        help='File pattern to match (default: env FILE_PATTERN or *.py)')
    parser.add_argument('--tag', default=os.environ.get('CODE_BLOCK_TAG', 'python'), 
                        help='Markdown code block tag (default: env CODE_BLOCK_TAG or python)')
    return parser.parse_args()

def main():
    # 解析 .env
    env_file = Path(__file__).parent / '.env'
    load_env(env_file)

    args = parse_args()

    target_folder = args.path
    if not target_folder:
        print('Error: TARGET_FOLDER is required. Set in .env or pass as first argument.')
        sys.exit(1)

    target_path = Path(target_folder)
    if not target_path.is_dir():
        print(f'Error: folder not found: {target_folder}')
        sys.exit(1)

    # 使用 pathlib 收集文件，并确保只匹配文件(排除目录)
    try:
        files = sorted([
            f for f in target_path.rglob(args.pattern)
            if f.is_file()
            and not any(
                part in DEFAULT_EXCLUDE_DIRS for part in f.relative_to(target_path).parts
            )
        ])
    except Exception as e:
        print(f'Error scanning directory: {e}')
        sys.exit(1)

    if not files:
        print(f'No files found matching pattern: {args.pattern}')
        sys.exit(1)

    # 准备输出路径
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)

    folder_name = target_path.name
    time_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f'{folder_name}-{time_str}.md'

    # 4. 流式写入，降低内存占用
    success_count = 0
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for fp in files:
            # 使用 as_posix() 保证路径分隔符永远是 / (符合 Markdown 和 URL 习惯)
            rel = fp.relative_to(target_path).as_posix()
            
            try:
                content = fp.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                print(f'[Warn] Skipped binary file: ./{rel}')
                continue
            except OSError as e:
                print(f'[Warn] Skipped unreadable file (Permission/Error): ./{rel} - {e}')
                continue

            out_f.write(f'## ./{rel}\n\n')
            max_run = max(len(m) for m in re.findall(r'`+', content)) if '`' in content else 0
            fence = '`' * max(3, max_run + 1)
            out_f.write(f'{fence}{args.tag}\n')
            out_f.write(content.rstrip('\n'))
            out_f.write(f'\n{fence}\n\n')
            success_count += 1

    print(f'✅ Done: {success_count}/{len(files)} files -> {output_file}')

if __name__ == '__main__':
    main()