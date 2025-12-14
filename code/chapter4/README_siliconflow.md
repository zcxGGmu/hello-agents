# 硅基流动 API 文本生成示例

本示例展示如何使用硅基流动（SiliconFlow）的 API 调用 DeepSeek-V3 模型进行文本生成。

## 文件说明

1. **`siliconflow_quickstart.py`** - 快速开始示例
   - 最简单的使用方式
   - 包含基本对话、流式输出、多轮对话等示例
   - 适合快速了解 API 使用方法

2. **`siliconflow_text_generation.py`** - 完整功能封装
   - 封装了 SiliconFlowClient 类
   - 提供更丰富的功能
   - 包含错误处理和多轮对话管理

3. **`siliconflow_config.py`** - 配置管理
   - 集中管理所有配置参数
   - 预定义了常用模型配置
   - 方便切换不同模型

## 快速开始

### 1. 安装依赖

```bash
pip install openai
```

### 2. 获取 API Key

1. 访问 [SiliconFlow 官网](https://cloud.siliconflow.cn/)
2. 注册账号并登录
3. 在控制台获取您的 API Key

### 3. 设置 API Key

方式一：设置环境变量（推荐）
```bash
export SILICONFLOW_API_KEY=your-api-key-here
```

方式二：在代码中直接设置
```python
# 修改代码中的 api_key 变量
api_key = "your-api-key-here"
```

### 4. 运行示例

```bash
# 快速开始示例
python siliconflow_quickstart.py

# 完整功能示例
python siliconflow_text_generation.py
```

## 代码示例

### 基本对话

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.siliconflow.cn/v1"
)

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3",
    messages=[
        {"role": "user", "content": "你好，请介绍一下自己。"}
    ],
    max_tokens=1000
)

print(response.choices[0].message.content)
```

### 流式输出

```python
stream = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3",
    messages=[
        {"role": "user", "content": "写一个关于春天的故事"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)
```

## 可用模型

| 模型名称 | 描述 | 备注 |
|---------|------|------|
| `deepseek-ai/DeepSeek-V3` | DeepSeek-V3 标准版 | 支持赠费余额和充值余额 |
| `Pro/deepseek-ai/DeepSeek-V3` | DeepSeek-V3 Pro 版 | 仅支持充值余额，性能更好 |
| `deepseek-ai/DeepSeek-R1` | DeepSeek-R1 推理模型 | 支持赠费余额和充值余额 |
| `Pro/deepseek-ai/DeepSeek-R1` | DeepSeek-R1 Pro 版 | 仅支持充值余额 |
| `Qwen/Qwen2.5-Coder-7B-Instruct` | Qwen 代码模型 7B | 适合代码生成任务 |
| `Qwen/Qwen2.5-Coder-32B-Instruct` | Qwen 代码模型 32B | 更强的代码能力 |

## 重要参数说明

- `max_tokens`: 最大输出 token 数，最大 16K
- `temperature`: 温度参数（0-2），控制输出的随机性
  - 0: 确定性输出，适合代码生成
  - 0.7: 平衡的输出，适合一般对话
  - 1.2-2: 高创造性输出，适合创意写作
- `top_p`: top-p 采样（0-1），控制输出的多样性
- `stream`: 是否使用流式输出

## 错误处理

常见错误及解决方案：

1. **401 错误**: API Key 无效
   - 检查 API Key 是否正确设置
   - 确认 API Key 未过期

2. **429 错误**: 请求频率超限
   - 降低请求频率
   - 考虑升级套餐

3. **404 错误**: 模型不存在
   - 检查模型名称是否正确
   - 确认模型是否可用

4. **400 错误**: 请求参数错误
   - 检查 max_tokens 是否在合理范围（1-16384）
   - 检查 temperature 是否在 0-2 之间

## 最佳实践

1. **合理设置参数**
   - 对于代码生成，使用较低的 temperature（0-0.3）
   - 对于创意写作，使用较高的 temperature（1.0-1.5）
   - 根据内容长度设置合适的 max_tokens

2. **处理长对话**
   - 使用多轮对话时，注意上下文长度限制（32K）
   - 必要时进行对话摘要或截断

3. **使用系统提示词**
   - 通过系统提示词设置角色和规则
   - 提高生成内容的质量和一致性

4. **优化成本**
   - Pro 版模型性能更好但仅支持充值余额
   - 根据需求选择合适的模型版本

## 相关链接

- [SiliconFlow 官网](https://cloud.siliconflow.cn/)
- [API 文档](https://docs.siliconflow.cn/cn/)
- [模型列表](https://docs.siliconflow.cn/cn/userguide/capabilities/text-generation)

## 许可证

本示例代码仅供学习和参考使用。