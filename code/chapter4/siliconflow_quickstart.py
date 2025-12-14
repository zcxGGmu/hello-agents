"""
硅基流动 API 快速开始示例
使用 DeepSeek-V3 模型进行文本生成

快速开始：
1. pip install openai
2. 修改下面的 api_key
3. 运行脚本：python siliconflow_quickstart.py
"""

from openai import OpenAI

# 配置 API Key（请替换为您的实际 API Key）
api_key = "your-siliconflow-api-key-here"

# 创建客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)

# 模型名称
# 注意：根据硅基流动文档，对于 DeepSeek-V3 模型
# - 普通版：deepseek-ai/DeepSeek-V3（支持赠费余额）
# - Pro 版：Pro/deepseek-ai/DeepSeek-V3（仅支持充值余额，性能更好）
model_name = "deepseek-ai/DeepSeek-V3"


def chat_completion_example():
    """对话补全示例"""
    print("=" * 50)
    print("硅基流动 DeepSeek-V3 对话示例")
    print("=" * 50)

    # 发送请求
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "你是一个专业的编程助手。"},
            {"role": "user", "content": "请用 Python 写一个计算斐波那契数列的函数。"}
        ],
        max_tokens=1000,
        temperature=0.7
    )

    # 打印结果
    print("用户：请用 Python 写一个计算斐波那契数列的函数。")
    print(f"\nDeepSeek-V3 回复：\n{response.choices[0].message.content}")

    # 显示 token 使用情况
    print(f"\nToken 使用情况：")
    print(f"- 输入 tokens: {response.usage.prompt_tokens}")
    print(f"- 输出 tokens: {response.usage.completion_tokens}")
    print(f"- 总计 tokens: {response.usage.total_tokens}")


def streaming_example():
    """流式输出示例"""
    print("\n" + "=" * 50)
    print("流式输出示例")
    print("=" * 50)

    print("用户：请解释一下什么是递归，并给出一个简单的例子。")
    print("\nDeepSeek-V3 回复（流式）：\n")

    # 创建流式请求
    stream = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": "请解释一下什么是递归，并给出一个简单的例子。"}
        ],
        stream=True,
        temperature=0.5
    )

    # 逐块接收并打印响应
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)

    print()  # 换行


def multi_turn_example():
    """多轮对话示例"""
    print("\n" + "=" * 50)
    print("多轮对话示例")
    print("=" * 50)

    # 对话历史
    messages = [
        {"role": "system", "content": "你是一个 Python 编程导师。"},
        {"role": "user", "content": "什么是装饰器？"},
        {"role": "assistant", "content": "装饰器是 Python 中的一种设计模式，它允许你在不修改原有函数代码的情况下，为函数添加新的功能。装饰器本质上是一个返回函数的函数。"},
        {"role": "user", "content": "能给我写一个简单的装饰器示例吗？"}
    ]

    print("对话历史：")
    print("用户：什么是装饰器？")
    print("助手：装饰器是 Python 中的一种设计模式，它允许你在不修改原有函数代码的情况下，为函数添加新的功能。装饰器本质上是一个返回函数的函数。")
    print("用户：能给我写一个简单的装饰器示例吗？")

    # 发送请求
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=1000,
        temperature=0.3
    )

    print(f"\nDeepSeek-V3 回复：\n{response.choices[0].message.content}")


def creative_writing_example():
    """创意写作示例（使用更高的温度）"""
    print("\n" + "=" * 50)
    print("创意写作示例")
    print("=" * 50)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": "请写一首关于春天的短诗（4行）。"}
        ],
        max_tokens=200,
        temperature=1.2  # 高温度增加创造性
    )

    print("用户：请写一首关于春天的短诗（4行）。")
    print(f"\nDeepSeek-V3 回复：\n{response.choices[0].message.content}")


def error_handling_example():
    """错误处理示例"""
    print("\n" + "=" * 50)
    print("错误处理示例")
    print("=" * 50)

    try:
        # 使用一个不存在的模型来演示错误处理
        response = client.chat.completions.create(
            model="non-existent-model",
            messages=[
                {"role": "user", "content": "Hello"}
            ]
        )
    except Exception as e:
        print(f"错误类型：{type(e).__name__}")
        print(f"错误信息：{e}")

        # 根据错误类型给出提示
        if "401" in str(e):
            print("\n提示：请检查您的 API Key 是否正确设置。")
        elif "404" in str(e):
            print("\n提示：模型名称不存在，请使用正确的模型名称。")
        elif "429" in str(e):
            print("\n提示：请求频率超限，请稍后重试或升级套餐。")


if __name__ == "__main__":
    # 检查 API Key
    if api_key == "your-siliconflow-api-key-here":
        print("⚠️  请先设置您的 SiliconFlow API Key！")
        print("\n设置步骤：")
        print("1. 访问 https://cloud.siliconflow.cn/")
        print("2. 注册账号并登录")
        print("3. 在控制台获取您的 API Key")
        print("4. 修改此文件中的 api_key 变量")
        print("\n或者设置环境变量：")
        print("export SILICONFLOW_API_KEY=your-api-key")
        exit(1)

    # 运行示例
    try:
        chat_completion_example()
        streaming_example()
        multi_turn_example()
        creative_writing_example()
        error_handling_example()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断。")
    except Exception as e:
        print(f"\n发生未预期的错误：{e}")
        print("\n请检查：")
        print("1. 网络连接是否正常")
        print("2. API Key 是否正确")
        print("3. 模型名称是否正确")