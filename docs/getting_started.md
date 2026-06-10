# 快速开始

SciCoverGen 让你在 5 分钟内为科研文档生成专业封面。

## 环境要求

- Python 3.8+
- 智谱开放平台 API Key（免费）

## 安装

### 方式一：pip 安装（推荐）

```bash
pip install scicovergen
```

### 方式二：源码安装

```bash
git clone https://github.com/luka9367/SciCoverGen.git
cd SciCoverGen
pip install -e .
```

## 获取 API Key

1. 访问 [智谱开放平台](https://open.bigmodel.cn/)
2. 注册账号（新用户免费）
3. 进入「API Keys」页面，创建新 Key
4. 复制 Key 备用

> 新用户注册即可免费领取 Cogview-3-Flash 图像生成额度，全程零费用。

## 支持的输入格式

| 格式 | 说明 | 额外依赖 |
|------|------|----------|
| `.md` | Markdown 文件（推荐） | 无 |
| `.txt` | 纯文本文件 | 无 |
| `.pdf` | PDF 论文 | `pip install pdfplumber` |
| 直接文本 | 直接传入字符串内容 | 无 |

## 生成封面

### Python 代码方式

```python
from scicovergen import SciCoverGen

# 设置 API Key（从环境变量读取更推荐）
import os
os.environ["ZHIPU_API_KEY"] = "your-api-key"

# 创建生成器
gen = SciCoverGen()

# 生成论文封面（支持 .md / .txt / .pdf）
gen.generate("your_paper.md", scene="paper_cover")
```

### 命令行方式

```bash
# 设置环境变量
export ZHIPU_API_KEY=your-api-key

# 生成论文封面
scicovergen paper.md --scene paper_cover

# 生成课题报告封面
scicovergen report.md --scene project_report

# 生成学术海报
scicovergen poster.md --scene academic_poster
```

## PDF 论文生成封面（详细教程）

SciCoverGen 支持**直接读取 PDF 论文文件**并自动生成封面，无需手动复制粘贴内容。

### 步骤 1：安装 PDF 支持

```bash
pip install pdfplumber
```

### 步骤 2：准备 PDF 论文

确保你的 PDF 是**文本型**（即文字可以被选中复制），而非扫描版图片。如果是扫描版 PDF，需要先使用 OCR 工具转换。

### 步骤 3：执行生成

**Python 代码：**

```python
from scicovergen import SciCoverGen
import os

os.environ["ZHIPU_API_KEY"] = "your-api-key"

gen = SciCoverGen()

# 直接传入 PDF 路径
result = gen.generate(
    source="C:/Users/你的论文.pdf",
    scene="paper_cover",
    output_dir="./covers"
)

print(f"封面已生成: {result}")
```

**命令行：**

```bash
# Windows PowerShell
$env:ZHIPU_API_KEY="your-api-key"
scicovergen "C:\Users\你的论文.pdf" --scene paper_cover -o ./covers

# Linux/macOS
export ZHIPU_API_KEY=your-api-key
scicovergen "论文.pdf" --scene paper_cover -o ./covers
```

### 步骤 4：查看结果

生成完成后，输出目录结构如下：

```
covers/
├── 论文标题_prompt.txt              # 自动生成的图像 Prompt（可查看/修改）
└── 论文标题_cover_20260610_113000.png  # 封面图像
```

### PDF 生成流程详解

```
PDF 论文文件
    ↓
pdfplumber 自动提取文本内容
    ↓
GLM-4-Flash 智能分析
    - 提取论文标题
    - 识别核心方法和数学对象
    - 判断学科领域（机器学习/图论/深度学习等）
    - 自动推荐配色和风格
    ↓
场景化 Prompt 构建
    - 根据学科选择专属视觉元素
    - 构建精准英文 Prompt（避免 AI 乱码）
    ↓
Cogview-3-Flash 生成封面图像
    ↓
保存到本地目录
```

### 常见问题

**Q: 为什么我的 PDF 无法读取？**
A: 请确认 PDF 是文本型而非扫描版。扫描版 PDF 中的文字是图片，无法被提取。建议使用 OCR 软件（如 Adobe Acrobat、ABBYY FineReader）先转换为可搜索 PDF。

**Q: 生成的封面不符合论文主题？**
A: 可以查看生成的 `_prompt.txt` 文件，了解自动分析的维度。如果需要调整，可以直接修改该 Prompt 后使用其他图像生成工具，或在 Python 中传入更详细的内容描述。

**Q: 支持中文论文吗？**
A: 完全支持！GLM-4-Flash 会自动分析中文论文内容，生成的 Prompt 为英文（因为图像生成模型对英文理解更好）。

## 三大场景说明

### 论文封面 (`paper_cover`)

适合学术论文、学位论文、期刊投稿等场景。

特点：
- 学术专业风格
- 突出数学/算法可视化
- 无文字（避免 AI 乱码）
- 冷色调为主

### 课题报告 (`project_report`)

适合科研项目报告、开题报告、结题报告等场景。

特点：
- 简洁结构化设计
- 数据图表元素
- 现代商务风格

### 学术海报 (`academic_poster`)

适合学术会议海报、展板、宣传材料等场景。

特点：
- 视觉冲击力强
- 信息丰富
- 适合大幅展示

## 下一步

- 查看 [API 参考](api_reference.md) 了解完整接口
- 查看 [示例](../examples/) 获取完整代码示例
- 提交 Issue 反馈问题或建议
