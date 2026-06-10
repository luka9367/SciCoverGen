# API 参考

## SciCoverGen 类

主生成器类，提供封面生成的核心功能。

### 构造函数

```python
SciCoverGen(api_key=None, output_dir="./scicovergen_output")
```

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `api_key` | str | None | 智谱 API Key，None 时从环境变量读取 |
| `output_dir` | str | "./scicovergen_output" | 默认输出目录 |

**示例：**

```python
from scicovergen import SciCoverGen

# 从环境变量读取 API Key
gen = SciCoverGen()

# 直接传入 API Key
gen = SciCoverGen(api_key="your-api-key")

# 指定输出目录
gen = SciCoverGen(output_dir="./my_covers")
```

### generate 方法

```python
generate(source, scene="paper_cover", output_dir=None, save_prompt=True) -> str
```

生成单个封面。

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `source` | str | 必填 | 内容源（文件路径或文本） |
| `scene` | str | "paper_cover" | 场景类型 |
| `output_dir` | str | None | 输出目录（覆盖构造函数设置） |
| `save_prompt` | bool | True | 是否保存生成的 prompt |

**返回值：**

生成图像的本地文件路径，失败返回 None。

**示例：**

```python
# 基本用法
path = gen.generate("paper.md")

# 指定场景
path = gen.generate("report.md", scene="project_report")

# 自定义输出目录
path = gen.generate("poster.md", scene="academic_poster", output_dir="./posters")
```

### generate_batch 方法

```python
generate_batch(sources, scene="paper_cover", output_dir=None) -> list
```

批量生成封面。

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `sources` | list | 必填 | 内容源列表 |
| `scene` | str | "paper_cover" | 场景类型 |
| `output_dir` | str | None | 输出目录 |

**返回值：**

成功生成的文件路径列表。

**示例：**

```python
papers = ["paper1.md", "paper2.md", "paper3.md"]
results = gen.generate_batch(papers, scene="paper_cover")
```

## quick_generate 函数

快捷函数，一行代码生成封面。

```python
quick_generate(source, api_key=None, scene="paper_cover", output_dir=None) -> str
```

**示例：**

```python
from scicovergen import quick_generate

path = quick_generate("paper.md", api_key="your-key")
```

## CLI 命令

### 基本命令

```bash
scicovergen <source> [options]
```

### 选项

| 选项 | 简写 | 说明 |
|------|------|------|
| `--scene` | `-s` | 场景类型 |
| `--output` | `-o` | 输出目录 |
| `--api-key` | `-k` | API Key |
| `--no-prompt` | | 不保存 prompt 文件 |
| `--version` | `-v` | 显示版本 |

### 示例

```bash
# 论文封面
scicovergen paper.md -s paper_cover

# 课题报告
scicovergen report.md -s project_report -o ./reports

# 学术海报
scicovergen poster.md -s academic_poster -k your-api-key
```

## 场景类型

| 场景 | 说明 | 适用场景 |
|------|------|----------|
| `paper_cover` | 论文封面 | 学术论文、学位论文 |
| `project_report` | 课题报告封面 | 项目报告、开题/结题报告 |
| `academic_poster` | 学术海报 | 会议海报、展板 |

## 环境变量

| 变量名 | 说明 |
|--------|------|
| `ZHIPU_API_KEY` | 智谱 API Key |
