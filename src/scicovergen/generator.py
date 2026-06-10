"""
SciCoverGen 主生成器

整合分析器、Prompt 构建器和 API 客户端，
提供简洁的接口供用户一键生成科研封面。
"""

import os
from typing import Optional

from .analyzer import ContentAnalyzer
from .api_client import ZhipuClient
from .config import Config
from .prompts import LLMPromptBuilder, PromptBuilder
from .utils import (
    ensure_dir,
    get_output_path,
    read_file,
    read_pdf,
    slugify,
)


class SciCoverGen:
    """
    科研封面生成器主类

    使用示例:
        >>> from scicovergen import SciCoverGen
        >>> gen = SciCoverGen(api_key="your-api-key")
        >>> gen.generate("paper.md", scene="paper_cover")
    """

    def __init__(self, api_key: Optional[str] = None, output_dir: Optional[str] = None):
        """
        初始化生成器

        Args:
            api_key: 智谱 API Key，默认从环境变量 ZHIPU_API_KEY 读取
            output_dir: 输出目录，默认 ./scicovergen_output
        """
        self.client = ZhipuClient(api_key)
        self.analyzer = ContentAnalyzer(self.client)
        self.output_dir = output_dir or Config.DEFAULT_OUTPUT_DIR
        ensure_dir(self.output_dir)

    def generate(
        self,
        source: str,
        scene: str = "paper_cover",
        output_dir: Optional[str] = None,
        save_prompt: bool = True,
    ) -> Optional[str]:
        """
        生成科研封面

        Args:
            source: 内容源（文件路径或直接文本）
            scene: 场景类型
                - "paper_cover": 论文封面
                - "project_report": 课题报告封面
                - "academic_poster": 学术海报
            output_dir: 输出目录，默认使用初始化时的目录
            save_prompt: 是否保存生成的 prompt

        Returns:
            生成图像的本地文件路径，失败返回 None
        """
        # 1. 读取内容
        print(f"📖 正在读取内容: {source}")
        content = self._load_content(source)
        if not content:
            print("❌ 无法读取内容")
            return None
        print(f"   ✅ 读取完成，共 {len(content)} 字符")

        # 2. 分析内容
        print(f"\n🔍 正在分析内容（场景: {scene}）...")
        analysis = self.analyzer.analyze(content, scene=scene)
        print(f"   ✅ 分析完成")
        print(f"   📌 标题: {analysis.get('title', 'N/A')}")
        print(f"   🎨 配色: {analysis.get('palette', 'N/A')}")
        print(f"   ✏️ 风格: {analysis.get('style', 'N/A')}")

        # 3. 构建 Prompt
        print(f"\n✍️ 正在构建生成 Prompt...")
        prompt = self._build_prompt(analysis, scene)

        # 确定输出目录
        out_dir = output_dir or self.output_dir
        ensure_dir(out_dir)

        # 保存 prompt
        if save_prompt:
            prompt_path = os.path.join(
                out_dir, f"{slugify(analysis.get('title', 'prompt'))}_prompt.txt"
            )
            with open(prompt_path, "w", encoding="utf-8") as f:
                f.write(prompt)
            print(f"   ✅ Prompt 已保存: {prompt_path}")

        # 4. 生成图像
        print(f"\n🎨 正在调用 Cogview-3-Flash 生成图像...")
        scene_config = Config.SCENE_CONFIGS.get(scene, Config.SCENE_CONFIGS["paper_cover"])
        image_url = self.client.generate_image(
            prompt=prompt,
            size=scene_config["size"],
        )

        if not image_url:
            print("❌ 图像生成失败")
            return None

        print(f"   ✅ 图像生成成功")

        # 5. 下载保存
        output_path = get_output_path(
            analysis.get("title", "cover"),
            out_dir,
            suffix=scene.replace("_", "-")
        )

        if self.client.download_image(image_url, output_path):
            print(f"\n🎉 封面生成完成!")
            print(f"   📁 保存路径: {output_path}")
            print(f"   🌐 在线预览: {image_url}")
            return output_path
        else:
            print(f"\n⚠️ 本地保存失败，但图像已生成")
            print(f"   🌐 在线URL: {image_url}")
            return None

    def generate_batch(
        self,
        sources: list,
        scene: str = "paper_cover",
        output_dir: Optional[str] = None,
    ) -> list:
        """
        批量生成封面

        Args:
            sources: 内容源列表
            scene: 场景类型
            output_dir: 输出目录

        Returns:
            成功生成的文件路径列表
        """
        results = []
        for i, source in enumerate(sources, 1):
            print(f"\n{'='*60}")
            print(f"📦 批量生成 [{i}/{len(sources)}]")
            print(f"{'='*60}")
            result = self.generate(source, scene=scene, output_dir=output_dir)
            if result:
                results.append(result)
        return results

    def _load_content(self, source: str) -> Optional[str]:
        """加载内容"""
        # 如果是文件路径
        if os.path.isfile(source):
            if source.lower().endswith('.pdf'):
                return read_pdf(source)
            else:
                return read_file(source)
        else:
            # 直接作为文本内容
            return source

    def _build_prompt(self, analysis: dict, scene: str) -> str:
        """根据场景构建 Prompt，优先使用 LLM 动态生成"""
        print("   🧠 调用 GLM-4-Flash 生成高质量 Prompt...")
        return LLMPromptBuilder.build_prompt(analysis, scene, self.client)


def quick_generate(
    source: str,
    api_key: Optional[str] = None,
    scene: str = "paper_cover",
    output_dir: Optional[str] = None,
) -> Optional[str]:
    """
    快速生成封面（单行调用）

    Args:
        source: 内容源（文件路径或文本）
        api_key: API Key
        scene: 场景类型
        output_dir: 输出目录

    Returns:
        生成的图像路径
    """
    gen = SciCoverGen(api_key=api_key, output_dir=output_dir)
    return gen.generate(source, scene=scene)
