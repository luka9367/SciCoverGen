"""
配置管理模块
"""

import os
from typing import Optional


class Config:
    """全局配置类"""

    # 智谱开放平台 API 配置
    ZHIPU_API_BASE: str = "https://open.bigmodel.cn/api/paas/v4"
    GLM_MODEL: str = "glm-4-flash"
    COGVIEW_MODEL: str = "cogview-3-flash"

    # 默认图像尺寸
    DEFAULT_IMAGE_SIZE: str = "1024x1024"

    # 场景默认配置
    SCENE_CONFIGS = {
        "paper_cover": {
            "size": "1024x1024",
            "temperature": 0.7,
            "max_tokens": 2000,
        },
        "project_report": {
            "size": "1024x1024",
            "temperature": 0.7,
            "max_tokens": 2000,
        },
        "academic_poster": {
            "size": "1024x1024",
            "temperature": 0.8,
            "max_tokens": 2500,
        },
    }

    # 输出配置
    DEFAULT_OUTPUT_DIR: str = "./scicovergen_output"

    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """从环境变量获取 API Key"""
        api_key = os.environ.get("ZHIPU_API_KEY")
        if not api_key:
            raise ValueError(
                "请设置环境变量 ZHIPU_API_KEY\n"
                "获取方式：访问 https://open.bigmodel.cn/ 注册并申请 API Key\n"
                "新用户注册即可免费领取 Cogview-3-Flash 调用额度"
            )
        return api_key

    @classmethod
    def set_api_key(cls, api_key: str):
        """设置 API Key"""
        os.environ["ZHIPU_API_KEY"] = api_key
