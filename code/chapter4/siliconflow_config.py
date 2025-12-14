"""
硅基流动 API 配置文件
集中管理所有配置参数
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class SiliconFlowConfig:
    """硅基流动 API 配置类"""

    # API 配置
    api_key: Optional[str] = None
    base_url: str = "https://api.siliconflow.cn/v1"

    # 模型配置
    model_name: str = "deepseek-ai/DeepSeek-V3"  # 默认使用 DeepSeek-V3
    max_tokens: int = 2000  # 最大输出 token 数（最大 16K）
    temperature: float = 0.7  # 温度参数（0-2）
    top_p: float = 0.95  # top-p 采样参数（0-1）

    # 请求配置
    timeout: int = 60  # 请求超时时间（秒）
    retry_times: int = 3  # 重试次数

    def __post_init__(self):
        """初始化后处理"""
        # 从环境变量获取 API Key（如果未在参数中指定）
        if not self.api_key:
            self.api_key = os.getenv("SILICONFLOW_API_KEY")

    def validate(self) -> bool:
        """验证配置是否有效"""
        if not self.api_key:
            print("错误：API Key 未设置")
            return False
        if not self.base_url:
            print("错误：base_url 未设置")
            return False
        if not self.model_name:
            print("错误：model_name 未设置")
            return False
        if self.max_tokens <= 0 or self.max_tokens > 16384:
            print("错误：max_tokens 必须在 1-16384 之间")
            return False
        if self.temperature < 0 or self.temperature > 2:
            print("错误：temperature 必须在 0-2 之间")
            return False
        if self.top_p <= 0 or self.top_p > 1:
            print("错误：top_p 必须在 0-1 之间")
            return False
        return True

    def get_headers(self) -> dict:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }


# 预定义的模型配置
MODEL_CONFIGS = {
    # DeepSeek 系列
    "deepseek-v3": {
        "model_name": "deepseek-ai/DeepSeek-V3",
        "description": "DeepSeek-V3 标准版（支持赠费余额）",
        "recommended_max_tokens": 2000,
        "context_length": 32768
    },
    "deepseek-v3-pro": {
        "model_name": "Pro/deepseek-ai/DeepSeek-V3",
        "description": "DeepSeek-V3 Pro 版（仅充值余额，性能更好）",
        "recommended_max_tokens": 4000,
        "context_length": 32768
    },
    "deepseek-r1": {
        "model_name": "deepseek-ai/DeepSeek-R1",
        "description": "DeepSeek-R1 推理模型（支持赠费余额）",
        "recommended_max_tokens": 2000,
        "context_length": 32768
    },
    "deepseek-r1-pro": {
        "model_name": "Pro/deepseek-ai/DeepSeek-R1",
        "description": "DeepSeek-R1 Pro 推理模型（仅充值余额）",
        "recommended_max_tokens": 4000,
        "context_length": 32768
    },
    # 其他可用模型
    "qwen-coder-7b": {
        "model_name": "Qwen/Qwen2.5-Coder-7B-Instruct",
        "description": "Qwen2.5-Coder 7B 代码模型",
        "recommended_max_tokens": 2000,
        "context_length": 32768
    },
    "qwen-coder-32b": {
        "model_name": "Qwen/Qwen2.5-Coder-32B-Instruct",
        "description": "Qwen2.5-Coder 32B 代码模型",
        "recommended_max_tokens": 4000,
        "context_length": 32768
    }
}


def get_default_config() -> SiliconFlowConfig:
    """获取默认配置"""
    return SiliconFlowConfig()


def create_config(
    api_key: Optional[str] = None,
    model: str = "deepseek-v3",
    **kwargs
) -> SiliconFlowConfig:
    """
    创建配置对象

    Args:
        api_key: API 密钥
        model: 模型名称（可选值见 MODEL_CONFIGS）
        **kwargs: 其他配置参数

    Returns:
        SiliconFlowConfig 配置对象
    """
    # 从预定义配置获取模型名称
    model_config = MODEL_CONFIGS.get(model, MODEL_CONFIGS["deepseek-v3"])

    config = SiliconFlowConfig(
        api_key=api_key,
        model_name=model_config["model_name"],
        **kwargs
    )

    # 设置推荐的最大 token 数
    if "recommended_max_tokens" in model_config:
        config.max_tokens = model_config["recommended_max_tokens"]

    return config


def list_available_models():
    """列出所有可用模型"""
    print("可用的模型配置：")
    print("=" * 60)
    for key, config in MODEL_CONFIGS.items():
        print(f"配置名: {key}")
        print(f"模型名称: {config['model_name']}")
        print(f"描述: {config['description']}")
        print(f"推荐最大 tokens: {config['recommended_max_tokens']}")
        print(f"上下文长度: {config['context_length']}")
        print("-" * 60)


# 使用示例
if __name__ == "__main__":
    # 列出可用模型
    list_available_models()

    # 创建配置示例
    print("\n创建配置示例：")
    print("-" * 40)

    # 使用环境变量 API Key
    config1 = get_default_config()
    print(f"默认模型: {config1.model_name}")

    # 使用特定模型
    config2 = create_config(
        api_key="your-api-key",
        model="deepseek-v3-pro",
        temperature=0.8
    )
    print(f"Pro 模型: {config2.model_name}")

    # 验证配置
    print(f"\n配置验证: {config1.validate()}")