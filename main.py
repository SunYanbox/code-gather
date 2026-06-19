import os
import re
import sys
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

DEFAULT_EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.idea', '.vscode'}


def parse_args():
    parser = argparse.ArgumentParser(description='Combine files into a single Markdown file.')
    parser.add_argument('path', nargs='?', default='',
                        help='Target folder to scan')
    parser.add_argument('--pattern', default=os.environ.get('FILE_PATTERN', '*.py'),
                        help='File pattern to match (default: env FILE_PATTERN or *.py)')
    parser.add_argument('--tag', default=os.environ.get('CODE_BLOCK_TAG', 'python'),
                        help='Markdown code block tag (default: env CODE_BLOCK_TAG or python)')
    parser.add_argument('--gui', action='store_true',
                        help='Force GUI mode')
    return parser.parse_args()


def scan_and_format(target_path: Path, pattern: str, tag: str) -> tuple[str, int, int]:
    """Scan folder and return (markdown_content, success_count, total_count)."""
    files = sorted([
        f for f in target_path.rglob(pattern)
        if f.is_file()
        and not any(
            part in DEFAULT_EXCLUDE_DIRS for part in f.relative_to(target_path).parts
        )
    ])

    lines = []
    success_count = 0
    for fp in files:
        rel = fp.relative_to(target_path).as_posix()
        try:
            content = fp.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            print(f'[Warn] Skipped binary file: ./{rel}')
            continue
        except OSError as e:
            print(f'[Warn] Skipped unreadable file: ./{rel} - {e}')
            continue

        lines.append(f'## ./{rel}\n')
        max_run = max(len(m) for m in re.findall(r'`+', content)) if '`' in content else 0
        fence = '`' * max(3, max_run + 1)
        lines.append(f'{fence}{tag}\n')
        lines.append(content.rstrip('\n'))
        lines.append(f'\n{fence}\n\n')
        success_count += 1

    return ''.join(lines), success_count, len(files)


def save_output(content: str, folder_name: str) -> Path:
    """Save content to output/ folder and return the output path."""
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    time_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f'{folder_name}-{time_str}.md'
    output_file.write_text(content, encoding='utf-8')
    return output_file


def gui():
    """Launch tkinter GUI for folder selection and preview."""
    import tkinter as tk
    from tkinter import filedialog, scrolledtext, messagebox

    root = tk.Tk()
    root.title('文件整理 — 文件夹代码合并')
    root.geometry('920x720')
    root.minsize(600, 400)

    # ── Top frame: folder selection ──────────────────────────
    top_frame = tk.Frame(root)
    top_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

    tk.Label(top_frame, text='📁 已选择:').pack(side=tk.LEFT)
    folder_label = tk.Label(top_frame, text='（尚未选择）', fg='gray', anchor='w')
    folder_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

    select_btn = tk.Button(top_frame, text='选择文件夹', command=lambda: select_folder())
    select_btn.pack(side=tk.RIGHT)

    # ── Text area ────────────────────────────────────────────
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED,
                                          font=('Consolas', 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # ── Status bar ───────────────────────────────────────────
    status_var = tk.StringVar(value='请点击上方 "选择文件夹" 按钮开始')
    status_bar = tk.Label(root, textvariable=status_var, fg='gray', anchor='w')
    status_bar.pack(fill=tk.X, padx=10, pady=(0, 5))

    # ── Bottom frame: action buttons ─────────────────────────
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

    current_content = ['']
    current_folder_name = ['']

    def select_folder():
        folder = filedialog.askdirectory(title='选择要扫描的文件夹')
        if not folder:
            return
        folder_path = Path(folder)
        current_folder_name[0] = folder_path.name
        folder_label.config(text=str(folder_path), fg='black')

        status_var.set(f'正在扫描 {folder_path.name} ...')
        root.update()

        # 用 .env 中的 pattern/tag 或默认值
        pattern = os.environ.get('FILE_PATTERN', '*.py')
        tag = os.environ.get('CODE_BLOCK_TAG', 'python')

        try:
            content, ok, total = scan_and_format(folder_path, pattern, tag)
            current_content[0] = content

            text_area.config(state=tk.NORMAL)
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, content)
            text_area.config(state=tk.DISABLED)

            status_var.set(f'✅ 已扫描: {ok}/{total} 个文件，共 {len(content):,} 字符')
        except Exception as e:
            messagebox.showerror('扫描出错', str(e))
            status_var.set('❌ 扫描失败')

    def copy_to_clipboard():
        if not current_content[0]:
            messagebox.showinfo('提示', '还没有内容，请先选择文件夹')
            return
        root.clipboard_clear()
        root.clipboard_append(current_content[0])
        status_var.set(f'📋 已复制 {len(current_content[0]):,} 字符到剪贴板')

    def save_to_output():
        if not current_content[0]:
            messagebox.showinfo('提示', '还没有内容，请先选择文件夹')
            return
        try:
            path = save_output(current_content[0], current_folder_name[0] or 'unknown')
            status_var.set(f'💾 已保存到: {path}')
            messagebox.showinfo('保存成功', f'文件已保存到:\n{path}')
        except Exception as e:
            messagebox.showerror('保存失败', str(e))

    # Buttons
    copy_btn = tk.Button(bottom_frame, text='📋 复制到剪贴板', command=copy_to_clipboard,
                         font=('', 10), padx=5)
    copy_btn.pack(side=tk.LEFT, padx=(0, 10))

    save_btn = tk.Button(bottom_frame, text='💾 保存到 output', command=save_to_output,
                         font=('', 10), padx=5)
    save_btn.pack(side=tk.LEFT, padx=(0, 10))

    reselect_btn = tk.Button(bottom_frame, text='🔄 重新选择', command=select_folder,
                             font=('', 10), padx=5)
    reselect_btn.pack(side=tk.LEFT)

    # 如果 .env 中有 TARGET_FOLDER，自动执行扫描
    env_folder = os.environ.get('TARGET_FOLDER', '')
    if env_folder:
        def auto_scan():
            folder_path = Path(env_folder)
            folder_label.config(text=str(folder_path), fg='black')
            current_folder_name[0] = folder_path.name

            if not folder_path.is_dir():
                status_var.set(f'⚠️ .env 中的路径无效: {env_folder}')
                return

            pattern = os.environ.get('FILE_PATTERN', '*.py')
            tag = os.environ.get('CODE_BLOCK_TAG', 'python')
            status_var.set(f'正在扫描 {folder_path.name} ...')
            root.update()

            try:
                content, ok, total = scan_and_format(folder_path, pattern, tag)
                current_content[0] = content
                text_area.config(state=tk.NORMAL)
                text_area.delete('1.0', tk.END)
                text_area.insert(tk.END, content)
                text_area.config(state=tk.DISABLED)
                status_var.set(f'✅ 已扫描: {ok}/{total} 个文件，共 {len(content):,} 字符')
            except Exception as e:
                messagebox.showerror('扫描出错', str(e))
                status_var.set('❌ 扫描失败')

        root.after(100, auto_scan)

    root.mainloop()


def main():
    # 加载 .env
    env_file = Path(__file__).parent / '.env'
    load_dotenv(env_file)

    args = parse_args()

    # 判定模式：传了路径参数 → CLI；否则 → GUI
    if args.gui or not args.path:
        gui()
        return

    target_path = Path(args.path)
    if not target_path.is_dir():
        print(f'Error: folder not found: {args.path}')
        sys.exit(1)

    content, ok, total = scan_and_format(target_path, args.pattern, args.tag)

    output_file = save_output(content, target_path.name)
    print(f'[OK] Done: {ok}/{total} files -> {output_file}')


if __name__ == '__main__':
    main()
