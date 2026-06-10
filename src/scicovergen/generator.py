"""
SciCoverGen 主生成器

整合分析器、Prompt 构建器、API 客户端和代码绘图后端，
支持四种生成模式：
- image:      文生图（Cogview-3-Flash），适合概念性配图
- diagram:    代码精确绘图（Matplotlib），适合算法流程图
- data_plot:  数据转绘图（8种顶会预建风格），适合实验图表
- image_repro: 图像复现（分析配图风格并 matplotlib 还原），适合复现论文图

使用示例:
    >>> from scicovergen import SciCoverGen
    >>> gen = SciCoverGen(api_key="your-api-key")
    >>> gen.generate("paper.pdf", mode="image", style="conference_diagram")
    >>> gen.generate("paper.pdf", mode="diagram")
    >>> gen.generate(data_dict, mode="data_plot", style="bar_paired_delta")
    >>> gen.generate("reference.png", mode="image_repro")
"""

import os
from typing import Optional, Dict, Any

from .analyzer import ContentAnalyzer
from .api_client import ZhipuClient
from .config import Config
from .diagram_renderer import render_diagram_from_architecture
from .plot_generator import PlotGenerator
from .plot_reproducer import PlotReproducer
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
    科研封面/配图生成器主类
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
        source,
        scene: str = "paper_cover",
        mode: str = "image",
        style: str = "artistic",
        output_dir: Optional[str] = None,
        save_prompt: bool = True,
        plot_data: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """
        生成科研配图

        Args:
            source: 内容源（文件路径、直接文本、数据字典或图像路径，取决于 mode）
            scene: 场景类型 (paper_cover/project_report/academic_poster)
            mode: 生成模式
                - "image":       文生图（调用 Cogview-3-Flash）
                - "diagram":     代码精确绘图（Matplotlib 矢量流程图）
                - "data_plot":   数据转绘图（8种顶会预建风格 matplotlib 图表）
                - "image_repro": 图像复现（分析配图风格并 matplotlib 还原）
            style: 风格类型
                - image 模式: "artistic" | "conference_diagram"
                - data_plot 模式: "bar_paired_delta" | "bar_grouped_hatch" |
                  "line_confidence_band" | "line_training_curve" |
                  "line_loss_with_inset" | "scatter_tsne_cluster" |
                  "scatter_broken_axis" | "radar_dual_series"
            output_dir: 输出目录，默认使用初始化时的目录
            save_prompt: 是否保存生成的 prompt（仅 image 模式）
            plot_data: 数据字典（仅 data_plot 模式，也可直接通过 source 传入）

        Returns:
            生成图像的本地文件路径，失败返回 None
        """
        if mode == "diagram":
            return self._generate_diagram(source, scene, output_dir)
        elif mode == "data_plot":
            return self._generate_data_plot(source, style, output_dir, plot_data)
        elif mode == "image_repro":
            return self._generate_image_repro(source, output_dir)
        else:
            return self._generate_image(source, scene, style, output_dir, save_prompt)

    def _generate_image(
        self,
        source: str,
        scene: str = "paper_cover",
        style: str = "artistic",
        output_dir: Optional[str] = None,
        save_prompt: bool = True,
    ) -> Optional[str]:
        """文生图模式（原有流程）"""
        # 1. 读取内容
        print(f"[READ] 正在读取内容: {source}")
        content = self._load_content(source)
        if not content:
            print("[ERROR] 无法读取内容")
            return None
        print(f"[OK] 读取完成，共 {len(content)} 字符")

        # 2. 分析内容
        print(f"[ANALYZE] 正在分析内容（场景: {scene}）...")
        analysis = self.analyzer.analyze(content, scene=scene)
        print(f"[OK] 分析完成")
        print(f"  - 标题: {analysis.get('title', 'N/A')}")
        print(f"  - 配色: {analysis.get('palette', 'N/A')}")
        print(f"  - 风格: {analysis.get('style', 'N/A')}")

        # 3. 构建 Prompt
        print(f"[PROMPT] 正在构建生成 Prompt（风格: {style}）...")
        prompt = LLMPromptBuilder.build_prompt(analysis, scene, self.client, style=style)

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
            print(f"[OK] Prompt 已保存: {prompt_path}")

        # 4. 生成图像
        print(f"[GENERATE] 正在调用 Cogview-3-Flash 生成图像...")
        scene_config = Config.SCENE_CONFIGS.get(scene, Config.SCENE_CONFIGS["paper_cover"])
        image_url = self.client.generate_image(
            prompt=prompt,
            size=scene_config["size"],
        )

        if not image_url:
            print("[ERROR] 图像生成失败")
            return None

        print(f"[OK] 图像生成成功")

        # 5. 下载保存
        output_path = get_output_path(
            analysis.get("title", "cover"),
            out_dir,
            suffix=scene.replace("_", "-")
        )

        if self.client.download_image(image_url, output_path):
            print(f"[DONE] 封面生成完成!")
            print(f"  - 保存路径: {output_path}")
            print(f"  - 在线预览: {image_url}")
            return output_path
        else:
            print(f"[WARN] 本地保存失败，但图像已生成")
            print(f"  - 在线URL: {image_url}")
            return None

    def _generate_diagram(
        self,
        source: str,
        scene: str = "paper_cover",
        output_dir: Optional[str] = None,
    ) -> Optional[str]:
        """代码绘图模式（精确矢量流程图）"""
        # 1. 读取内容
        print(f"[READ] 正在读取内容: {source}")
        content = self._load_content(source)
        if not content:
            print("[ERROR] 无法读取内容")
            return None
        print(f"[OK] 读取完成，共 {len(content)} 字符")

        # 2. 分析内容（获取标题等元信息）
        print(f"[ANALYZE] 正在分析内容...")
        analysis = self.analyzer.analyze(content, scene=scene)
        title = analysis.get("title", "Algorithm Architecture")
        print(f"[OK] 分析完成，标题: {title}")

        # 3. 提取架构
        print(f"[ARCH] 正在提取算法架构...")
        architecture = self.analyzer.extract_architecture(content, title=title)
        print(f"[OK] 架构提取完成")
        print(f"  - Stages: {len(architecture.get('stages', []))}")
        print(f"  - Modules: {sum(len(s.get('modules', [])) for s in architecture.get('stages', []))}")
        print(f"  - Connections: {len(architecture.get('connections', []))}")

        # 确定输出目录
        out_dir = output_dir or self.output_dir
        ensure_dir(out_dir)

        # 4. 渲染流程图
        print(f"[RENDER] 正在渲染矢量流程图...")
        output_path = get_output_path(
            title,
            out_dir,
            suffix="diagram"
        )
        # 确保使用 .png 后缀
        if not output_path.endswith(".png"):
            output_path += ".png"

        try:
            render_diagram_from_architecture(architecture, output_path, figsize=(14, 10), dpi=300)
            print(f"[DONE] 流程图生成完成!")
            print(f"  - 保存路径: {output_path}")
            print(f"  - 格式: PNG 300dpi，可直接用于论文")
            return output_path
        except Exception as e:
            print(f"[ERROR] 流程图渲染失败: {e}")
            return None

    def _generate_data_plot(
        self,
        source,
        style: str,
        output_dir: Optional[str] = None,
        plot_data: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """数据转绘图模式（8种顶会预建风格）"""
        data = plot_data if plot_data is not None else source
        if not isinstance(data, dict):
            print("[ERROR] data_plot 模式需要传入数据字典")
            return None

        print(f"[PLOT] 数据转绘图（风格: {style}）...")
        out_dir = output_dir or self.output_dir
        ensure_dir(out_dir)

        from .plot_styles import list_styles
        if style not in list_styles():
            print(f"[ERROR] 未知绘图风格 '{style}'")
            print(f"  可用风格: {', '.join(list_styles())}")
            return None

        output_path = get_output_path(
            data.get("title", "plot"),
            out_dir,
            suffix=style
        )
        if not output_path.endswith(".png"):
            output_path += ".png"

        try:
            gen = PlotGenerator()
            gen.generate(data, style, output_path)
            print(f"[DONE] 图表生成完成!")
            print(f"  - 保存路径: {output_path}")
            print(f"  - 格式: PNG 300dpi，顶会风格")
            return output_path
        except Exception as e:
            print(f"[ERROR] 图表生成失败: {e}")
            return None

    def _generate_image_repro(
        self,
        source: str,
        output_dir: Optional[str] = None,
    ) -> Optional[str]:
        """图像复现模式（分析配图并 matplotlib 还原）"""
        if not os.path.isfile(source):
            print(f"[ERROR] image_repro 模式需要传入图像文件路径: {source}")
            return None

        print(f"[REPRO] 图像复现: {source}")
        out_dir = output_dir or self.output_dir
        ensure_dir(out_dir)

        output_path = get_output_path(
            os.path.splitext(os.path.basename(source))[0],
            out_dir,
            suffix="repro"
        )
        if not output_path.endswith(".png"):
            output_path += ".png"

        try:
            repro = PlotReproducer(api_client=self.client)
            repro.reproduce(source, output_path, use_llm=True)
            return output_path
        except Exception as e:
            print(f"[ERROR] 图像复现失败: {e}")
            return None

    def generate_batch(
        self,
        sources: list,
        scene: str = "paper_cover",
        mode: str = "image",
        style: str = "artistic",
        output_dir: Optional[str] = None,
    ) -> list:
        """
        批量生成配图

        Args:
            sources: 内容源列表
            scene: 场景类型
            mode: 生成模式 (image/diagram)
            style: 风格类型（仅 image 模式）
            output_dir: 输出目录

        Returns:
            成功生成的文件路径列表
        """
        results = []
        for i, source in enumerate(sources, 1):
            print(f"\n{'='*60}")
            print(f"[BATCH] 批量生成 [{i}/{len(sources)}]")
            print(f"{'='*60}")
            result = self.generate(
                source, scene=scene, mode=mode, style=style, output_dir=output_dir
            )
            if result:
                results.append(result)
        return results

    def _load_content(self, source: str) -> Optional[str]:
        """加载内容"""
        if os.path.isfile(source):
            if source.lower().endswith('.pdf'):
                return read_pdf(source)
            else:
                return read_file(source)
        else:
            return source


def quick_generate(
    source: str,
    api_key: Optional[str] = None,
    scene: str = "paper_cover",
    mode: str = "image",
    style: str = "artistic",
    output_dir: Optional[str] = None,
) -> Optional[str]:
    """
    快速生成配图（单行调用）

    Args:
        source: 内容源（文件路径或文本）
        api_key: API Key
        scene: 场景类型
        mode: 生成模式 (image/diagram)
        style: 风格类型（仅 image 模式）
        output_dir: 输出目录

    Returns:
        生成的图像路径
    """
    gen = SciCoverGen(api_key=api_key, output_dir=output_dir)
    return gen.generate(source, scene=scene, mode=mode, style=style)
