"""
工具函数模块
"""

import os
import re
from typing import Optional


def read_file(filepath: str) -> Optional[str]:
    """读取文件内容"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # 尝试其他编码
        with open(filepath, "r", encoding="gbk") as f:
            return f.read()
    except Exception as e:
        print(f"读取文件失败: {e}")
        return None


def read_pdf(filepath: str) -> Optional[str]:
    """读取 PDF 文件内容"""
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        return text.strip() if text else None
    except ImportError:
        print("请安装 pdfplumber: pip install pdfplumber")
        return None
    except Exception as e:
        print(f"读取 PDF 失败: {e}")
        return None


def slugify(text: str, max_length: int = 30) -> str:
    """将文本转换为安全的文件名"""
    # 保留中文字符和英文
    text = re.sub(r'[^\w\u4e00-\u9fff\s-]', '-', text)
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text[:max_length]


def ensure_dir(directory: str):
    """确保目录存在"""
    os.makedirs(directory, exist_ok=True)


def get_output_path(title: str, output_dir: str, suffix: str = "cover") -> str:
    """生成输出文件路径"""
    slug = slugify(title)
    timestamp = re.sub(r'[^\d]', '', __import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S'))
    filename = f"{slug}_{suffix}_{timestamp}.png"
    return os.path.join(output_dir, filename)
