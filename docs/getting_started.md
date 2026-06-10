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

## 第一个封面

### Python 代码方式

```python
from scicovergen import SciCoverGen

# 设置 API Key（从环境变量读取更推荐）
import os
os.environ["ZHIPU_API_KEY"] = "your-api-key"

# 创建生成器
gen = SciCoverGen()

# 生成论文封面
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

## 支持的输入格式

| 格式 | 说明 |
|------|------|
| `.md` | Markdown 文件（推荐） |
| `.txt` | 纯文本文件 |
| `.pdf` | PDF 论文（需安装 pdfplumber） |
| 直接文本 | 直接传入字符串内容 |

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
