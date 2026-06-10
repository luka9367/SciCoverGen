"""
SciCoverGen - 科研封面自动生成工具
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scicovergen",
    version="1.3.0",
    author="SciCoverGen Team",
    author_email="scicovergen@example.com",
    description="融合国内免费大模型能力，参考顶级学府研究经验，为 CS & AI 科研工作者提供一站式图片复现与生图解决方案",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luka9367/SciCoverGen",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "matplotlib>=3.5.0",
        "numpy>=1.20.0",
        "Pillow>=9.0.0",
    ],
    extras_require={
        "pdf": [
            "pdfplumber>=0.6.0",
        ],
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
        "all": [
            "pdfplumber>=0.6.0",
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "scicovergen=scicovergen.cli:main",
        ],
    },
    keywords="科研封面 论文封面 学术海报 图像生成 AI绘图 Cogview 智谱",
    project_urls={
        "Bug Reports": "https://github.com/luka9367/SciCoverGen/issues",
        "Source": "https://github.com/luka9367/SciCoverGen",
        "Documentation": "https://github.com/luka9367/SciCoverGen/tree/main/docs",
    },
)
