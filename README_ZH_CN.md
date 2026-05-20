# CodeGather

**CodeGather** 是一个轻量级的 Python 工具，用于递归扫描目标文件夹，收集所有匹配的源代码文件，并将它们整合为一份 Markdown 文档，方便分享、审查或供 LLM 使用。

## 功能

- 递归扫描任意文件夹中符合模式的文件
- 生成清晰的 Markdown 文档，以相对路径作为标题
- 可配置的代码块语言标签
- 支持通过 `.env` 文件或命令行参数配置
- 输出文件带有时间戳，便于版本追踪

## 使用方法

### 命令行

```bash
python main.py /path/to/target/folder "*.py" python
```

参数说明（按顺序）：
1. `TARGET_FOLDER` — 要扫描的目标文件夹路径（必填）
2. `FILE_PATTERN` — 匹配文件的 Glob 模式（可选，默认：`*.py`）
3. `CODE_BLOCK_TAG` — Markdown 代码块的语言标签（可选，默认：`python`）

### 使用 .env 配置

在项目根目录创建 `.env` 文件（参考 `.env.example`）：

```env
TARGET_FOLDER=/path/to/target/folder
FILE_PATTERN=*.py
CODE_BLOCK_TAG=python
```

然后直接运行：

```bash
python main.py
```

### Windows 快捷启动

```
run.cmd
```

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
