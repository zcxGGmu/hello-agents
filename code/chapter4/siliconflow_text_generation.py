"""
硅基流动 API 文本生成示例
使用 deepseek-ai/DeepSeek-V3 模型进行文本生成

安装依赖：
pip install openai

配置说明：
1. 从 https://cloud.siliconflow.cn/ 获取 API Key
2. 设置环境变量 SILICONFLOW_API_KEY 或在代码中直接设置
"""

import os
import sys
from typing import List, Optional, Union, Dict, Any
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


class SiliconFlowClient:
    """硅基流动 API 客户端封装"""

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.siliconflow.cn/v1"):
        """
        初始化硅基流动客户端

        Args:
            api_key: API 密钥，如果不提供将从环境变量 SILICONFLOW_API_KEY 获取
            base_url: API 基础 URL，默认为硅基流动的地址
        """
        self.api_key = api_key or os.getenv("SILICONFLOW_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API Key 未设置。请设置环境变量 SILICONFLOW_API_KEY "
                "或在初始化时传入 api_key 参数。\n"
                "获取 API Key：https://cloud.siliconflow.cn/"
            )

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=base_url
        )

        # DeepSeek-V3 模型名称（根据文档，支持普通版和 Pro 版）
        # 普通版：支持赠费余额和充值余额
        # Pro 版：仅支持充值余额，性能更好
        self.model_name = "deepseek-ai/DeepSeek-V3"
        # 如果您使用 Pro 版，可以使用："Pro/deepseek-ai/DeepSeek-V3"
        # self.model_name = "Pro/deepseek-ai/DeepSeek-V3"

    def generate_text(
        self,
        messages: List[ChatCompletionMessageParam],
        max_tokens: int = 2000,
        temperature: float = 0.7,
        top_p: float = 0.95,
        stream: bool = False,
        **kwargs
    ) -> Union[Any, None]:
        """
        生成文本

        Args:
            messages: 对话消息列表，格式为 [{"role": "user", "content": "..."}, ...]
            max_tokens: 最大生成 token 数，最大 16K
            temperature: 温度参数，控制随机性（0-2）
            top_p: top-p 采样参数（0-1）
            stream: 是否使用流式输出
            **kwargs: 其他参数

        Returns:
            如果 stream=False，返回完整的响应对象
            如果 stream=True，返回生成器，逐个产生响应块
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stream=stream,
                **kwargs
            )

            if stream:
                return response
            else:
                return response

        except Exception as e:
            print(f"请求失败: {e}")
            # 常见错误处理
            if "429" in str(e):
                print("错误：请求频率超限。请稍后重试或升级套餐。")
            elif "401" in str(e):
                print("错误：API Key 无效。请检查您的 API Key。")
            elif "400" in str(e):
                print("错误：请求参数错误。请检查输入参数。")
            return None

    def simple_chat(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Optional[str]:
        """
        简单的单轮对话

        Args:
            prompt: 用户输入的问题
            system_prompt: 系统提示词（可选）
            **kwargs: 传递给 generate_text 的其他参数

        Returns:
            生成的回复文本
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        response = self.generate_text(messages=messages, **kwargs)

        if response and response.choices:
            return response.choices[0].message.content
        return None

    def stream_chat(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ):
        """
        流式对话，实时输出生成内容

        Args:
            prompt: 用户输入
            system_prompt: 系统提示词（可选）
            **kwargs: 其他参数
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        response_stream = self.generate_text(
            messages=messages,
            stream=True,
            **kwargs
        )

        if response_stream:
            for chunk in response_stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

    def multi_turn_chat(self, conversation_history: List[ChatCompletionMessageParam], **kwargs) -> Optional[str]:
        """
        多轮对话

        Args:
            conversation_history: 对话历史，格式为 [{"role": "user", "content": "..."}, ...]
            **kwargs: 其他参数

        Returns:
            模型回复
        """
        response = self.generate_text(messages=conversation_history, **kwargs)

        if response and response.choices:
            return response.choices[0].message.content
        return None

    def get_usage_info(self):
        """获取账户信息（需要单独的 API 接口）"""
        # 这里可以添加获取账户余额和使用情况的代码
        # 根据 siliconflow 技能包，需要调用 userinfo 接口
        pass


def main():
    """主函数 - 示例用法"""

    # 创建客户端实例
    # 方式1：从环境变量获取 API Key
    # client = SiliconFlowClient()

    # 方式2：直接传入 API Key
    # 请替换为您的实际 API Key
    api_key = "your-siliconflow-api-key-here"
    client = SiliconFlowClient(api_key=api_key)

    print("=" * 60)
    print("硅基流动 DeepSeek-V3 文本生成示例")
    print("=" * 60)

    # 示例1：简单文本生成
    print("\n1. 简单文本生成示例：")
    print("-" * 40)

    prompt = "请用 Python 写一个快速排序算法，并添加详细的注释说明。"
    response = client.simple_chat(
        prompt=prompt,
        max_tokens=1000,
        temperature=0.3
    )

    if response:
        print(f"用户：{prompt}")
        print(f"DeepSeek-V3 回复：\n{response}")
    else:
        print("生成失败！")

    # 示例2：带系统提示词的对话
    print("\n2. 带系统提示词的对话示例：")
    print("-" * 40)

    system_prompt = "你是一个专业的 Python 编程助手，请提供清晰、简洁、高效的代码解决方案。"
    prompt = "如何使用 Python 读取和处理 JSON 文件？请提供代码示例。"

    response = client.simple_chat(
        prompt=prompt,
        system_prompt=system_prompt,
        max_tokens=800
    )

    if response:
        print(f"系统提示词：{system_prompt}")
        print(f"用户：{prompt}")
        print(f"DeepSeek-V3 回复：\n{response}")

    # 示例3：流式输出
    print("\n3. 流式输出示例：")
    print("-" * 40)

    prompt = "请解释一下什么是机器学习，并说明其主要类型。"
    print(f"用户：{prompt}")
    print("DeepSeek-V3 回复（流式）：")

    for chunk in client.stream_chat(prompt, max_tokens=1000):
        print(chunk, end='', flush=True)
    print()  # 换行

    # 示例4：多轮对话
    print("\n4. 多轮对话示例：")
    print("-" * 40)

    conversation = [
        {"role": "user", "content": "什么是 REST API？"},
        {"role": "assistant", "content": "REST API 是一种基于 HTTP 协议的 Web API 设计风格..."},
        {"role": "user", "content": "能给我一个具体的 Python 实现示例吗？"}
    ]

    response = client.multi_turn_chat(conversation, max_tokens=1000)

    if response:
        print("对话历史：")
        for msg in conversation[:-1]:
            print(f"{msg['role'].upper()}: {msg['content']}")
        print(f"USER: {conversation[-1]['content']}")
        print(f"DeepSeek-V3 回复：\n{response}")

    # 示例5：创意写作
    print("\n5. 创意写作示例（高温度）：")
    print("-" * 40)

    prompt = "写一个关于人工智能未来的简短科幻故事（200字左右）。"
    response = client.simple_chat(
        prompt=prompt,
        temperature=1.2,  # 高温度，增加创造性
        max_tokens=500
    )

    if response:
        print(f"用户：{prompt}")
        print(f"DeepSeek-V3 回复：\n{response}")


def test_model_info():
    """测试模型信息"""
    print("\n可用的 DeepSeek 模型：")
    print("- deepseek-ai/DeepSeek-V3 (当前使用)")
    print("- Pro/deepseek-ai/DeepSeek-V3 (Pro 版，仅充值余额)")
    print("- deepseek-ai/DeepSeek-R1")
    print("- Pro/deepseek-ai/DeepSeek-R1 (Pro 版)")
    print("- deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")
    print("- deepseek-ai/DeepSeek-R1-Distill-Qwen-14B")
    print("- deepseek-ai/DeepSeek-R1-Distill-Qwen-32B")
    print("\n注意：")
    print("- Pro 版模型仅支持充值余额支付")
    print("- 非 Pro 版模型支持赠费余额和充值余额支付")


if __name__ == "__main__":
    # 检查是否设置了 API Key
    if not os.getenv("SILICONFLOW_API_KEY") and "your-siliconflow-api-key-here" in api_key:
        print("\n⚠️  请先设置您的 SiliconFlow API Key！")
        print("\n设置方法：")
        print("1. 访问 https://cloud.siliconflow.cn/ 注册账号并获取 API Key")
        print("2. 设置环境变量：export SILICONFLOW_API_KEY=your-api-key")
        print("3. 或者直接在代码中修改 api_key 变量\n")
        test_model_info()
        sys.exit(1)

    # 运行示例
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断。")
    except Exception as e:
        print(f"\n发生错误：{e}")
        print("\n请检查：")
        print("1. API Key 是否正确设置")
        print("2. 网络连接是否正常")
        print("3. 模型名称是否正确")