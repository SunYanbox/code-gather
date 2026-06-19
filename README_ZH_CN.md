# CodeGather

**CodeGather** 是一个轻量级的 Python 工具，用于递归扫描目标文件夹，收集所有匹配的源代码文件，并将它们整合为一份 Markdown 文档，方便分享、审查或供 LLM 使用。

## 功能

- **GUI 模式** — 文件夹选择对话框、可滚动的预览界面、一键复制到剪贴板、保存到文件
- **CLI 模式** — 无头运行，适合脚本和自动化
- 递归扫描任意文件夹中符合模式的文件
- 生成清晰的 Markdown 文档，以相对路径作为标题
- 可配置的代码块语言标签
- 支持通过 `.env` 文件或命令行参数配置
- 输出文件带有时间戳，便于版本追踪

## 使用方法

### GUI 模式（默认）

直接运行即可打开交互窗口：

```bash
python main.py
```

在界面中：

1. 点击 **选择文件夹** 选取目标目录
2. 自动扫描并在可滚动的只读文本区展示结果（支持选中和复制）
3. 点击 **📋 复制到剪贴板** 一键复制全部内容
4. 点击 **💾 保存到 output** 将结果保存为 Markdown 到 `output/` 目录

如果在 `.env` 中设置了 `TARGET_FOLDER`，启动后会自动扫描该文件夹。

### 命令行模式

传入文件夹路径作为参数即可进入命令行模式：

```bash
python main.py /path/to/target/folder --pattern "*.py" --tag python
```

参数说明：

| 参数           | 说明                                               | 默认值                |
|----------------|----------------------------------------------------|-----------------------|
| `path`         | 要扫描的目标文件夹路径                             | (env `TARGET_FOLDER`) |
| `--pattern`    | 匹配文件的 Glob 模式                               | `*.py`                |
| `--tag`        | Markdown 代码块的语言标签                          | `python`              |
| `--gui`        | 强制使用 GUI 模式（即使传入了路径）                | —                     |

### 使用 .env 配置

在项目根目录创建 `.env` 文件（参考 `.env.example`）：

```env
TARGET_FOLDER=/path/to/target/folder
FILE_PATTERN=*.py
CODE_BLOCK_TAG=python
```

### Windows 快捷启动

```
run.cmd
```

不带参数时默认打开 GUI。如需 CLI 模式，请编辑脚本或直接在命令行传参运行。

## 输出

生成的文件保存在 `output/` 目录下，命名格式为：

```
output/{folder_name}-{YYYYMMDD_HHMMSS}.md
```

每个源文件的格式如下：

```markdown
## ./relative/path/to/file.py

\`\`\`python
文件内容
\`\`\`
```

## 环境要求

- Python 3.12+
- 无需第三方依赖

## 许可证

MIT
