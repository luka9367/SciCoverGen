"""
论文封面生成示例

演示如何使用 SciCoverGen 为学术论文生成专业封面。
"""

import os
import sys

# 添加项目源码路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from scicovergen import SciCoverGen


def main():
    """生成论文封面示例"""

    # 初始化生成器
    # 方式1: 直接传入 API Key
    # gen = SciCoverGen(api_key="your-api-key")

    # 方式2: 从环境变量读取 (推荐)
    # export ZHIPU_API_KEY=your-api-key
    gen = SciCoverGen()

    # 生成论文封面
    print("=" * 60)
    print("📄 论文封面生成示例")
    print("=" * 60)

    result = gen.generate(
        source="example_paper.md",      # 论文文件路径
        scene="paper_cover",             # 场景: 论文封面
        output_dir="./paper_output",     # 输出目录
    )

    if result:
        print(f"\n✅ 封面已生成: {result}")
    else:
        print("\n❌ 生成失败")


if __name__ == "__main__":
    main()
