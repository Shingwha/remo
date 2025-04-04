
# Remo

## 项目概述
Remo 是一个小型 Agent 项目，借助大语言模型（LLM）实现对话交互，同时支持调用多种工具来完成特定任务。它提供了工具集成、对话管理和记忆管理等功能，方便用户在对话过程中灵活使用各种工具和管理对话信息。

## 安装与配置
### 依赖安装
确保你的 Python 版本 >= 3.11，然后使用以下命令安装项目依赖：
```bash
uv pip install .
```
依赖信息在 `pyproject.toml` 文件中列出，主要包括：
```toml
[project]
name = "remo"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "openai>=1.70.0",
    "pydantic>=2.11.1",
    "requests",
]
```

### 配置 API 密钥
在使用 `OpenAIServer` 时，需要配置 API 密钥和基础 URL，示例如下：
```python
from src.core import Agent, OpenAIServer

llm = OpenAIServer(api_key="your_api_key", base_url="https://ark.cn-beijing.volces.com/api/v3", model_name="doubao-1-5-pro-32k-250115")
```

## 使用示例
以下是一个简单的使用示例，展示了如何创建一个智能助手并进行对话：
```python
from src.core import Agent, OpenAIServer
from src.tools.calculator import Calculator
from src.core import MemoryBank, Memory
import time

llm = OpenAIServer(api_key="", base_url="https://ark.cn-beijing.volces.com/api/v3", model_name="doubao-1-5-pro-32k-250115")

memorys = MemoryBank(storage_path="my_memory.json")
agent = Agent(llm=llm, tools=[Calculator()], memory_bank=memorys, system_prompt="你是一个用户的知心朋友，你很热情友善，你可以在回答中加入一些表情来活跃聊天氛围，请根据用户的指令，给出合适的回答，请不要主动说出prompt的内容，除非用户明确要求")

while True:
    query = input("请输入:")
    if query == "exit":
        break
    elif query == "clear":
        agent.conversation.clear()
    else:
        agent.generate(query)
```

## 代码结构
```
remo/
├── src/
│   ├── core/
│   │   ├── agent.py          # Agent核心逻辑
│   │   ├── llm.py            # 大语言模型接口
│   │   ├── message.py        # 对话消息管理
│   │   ├── prompt.py         # 提示信息管理
│   │   ├── tool.py           # 工具基类和工具执行逻辑
│   │   ├── utils.py          # 解析等工具
│   │   └── memory.py         # 记忆管理
│   └── tools/
│       ├── bocha.py          # Bocha 搜索工具
│       └── calculator.py     # 计算器工具
├── test.py                   # 测试脚本
├── pyproject.toml            # 项目依赖配置
└── .gitignore                # Git 忽略文件配置
```

## 功能特性
- **工具集成**：支持创建工具，创建示例详见 `Calculator`。你可以根据需要自定义工具，实现特定的功能。
- **工具调用格式**：采用 XML 风格的标签来格式化工具调用，确保工具使用的规范和解析的准确性。例如：
```xml
<read_file>
<path>src/main.js</path>
</read_file>
```
- **对话管理**：提供对话管理功能，能够记录用户和助手的消息，并支持对话的清空操作。你可以使用 `agent.conversation.clear()` 方法清空对话记录。
- **记忆管理**：支持记忆的添加、删除、更新和查询操作。记忆信息可以存储在本地文件中，方便后续使用。

## 注意事项
- 在使用工具时，请确保输入的参数符合工具的要求，避免出现解析错误。
- 在配置 API 密钥时，请将 `your_api_key` 替换为你自己的有效 API 密钥。
