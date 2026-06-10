"""
智谱开放平台 API 客户端

封装 GLM-4-Flash（文本分析）和 Cogview-3-Flash（图像生成）接口。
"""

import json
import time
from typing import Any, Dict, List, Optional

import requests

from .config import Config


class ZhipuClient:
    """智谱 API 客户端"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.get_api_key()
        self.base_url = Config.ZHIPU_API_BASE
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _post(self, endpoint: str, payload: Dict[str, Any], timeout: int = 120) -> Dict[str, Any]:
        """发送 POST 请求"""
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=payload, timeout=timeout)

        if response.status_code != 200:
            error_msg = f"API 请求失败 (HTTP {response.status_code})"
            try:
                error_detail = response.json()
                error_msg += f": {error_detail}"
            except:
                error_msg += f": {response.text}"
            raise APIError(error_msg)

        return response.json()

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """
        调用 GLM-4-Flash 进行文本生成/分析

        Args:
            messages: 对话消息列表
            model: 模型名称，默认 glm-4-flash
            temperature: 采样温度
            max_tokens: 最大生成 token 数

        Returns:
            生成的文本内容
        """
        payload = {
            "model": model or Config.GLM_MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        result = self._post("chat/completions", payload)
        return result["choices"][0]["message"]["content"]

    def generate_image(
        self,
        prompt: str,
        size: str = None,
        n: int = 1,
    ) -> Optional[str]:
        """
        调用 Cogview-3-Flash 生成图像

        Args:
            prompt: 图像生成提示词
            size: 图像尺寸，默认 1024x1024
            n: 生成图像数量

        Returns:
            生成图像的 URL，失败返回 None
        """
        payload = {
            "model": Config.COGVIEW_MODEL,
            "prompt": prompt,
            "size": size or Config.DEFAULT_IMAGE_SIZE,
            "n": n,
        }

        try:
            result = self._post("images/generations", payload, timeout=120)
            if "data" in result and len(result["data"]) > 0:
                return result["data"][0].get("url")
            return None
        except APIError as e:
            # 处理 429 限流
            if "429" in str(e) or "访问量过大" in str(e):
                time.sleep(3)
                result = self._post("images/generations", payload, timeout=120)
                if "data" in result and len(result["data"]) > 0:
                    return result["data"][0].get("url")
            raise

    def download_image(self, image_url: str, filepath: str) -> bool:
        """下载图像到本地"""
        try:
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()
            with open(filepath, "wb") as f:
                f.write(response.content)
            return True
        except Exception as e:
            print(f"下载图像失败: {e}")
            return False


class APIError(Exception):
    """API 调用异常"""
    pass
