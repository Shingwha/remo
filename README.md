# Remo

## 项目概述
Remo 是一个小型Agent项目，借助LLM实现对话交互，同时支持调用多种工具来完成特定任务。

## 功能特性
- **工具集成**：支持创建工具，创建示例详见 `Calculator`。
- **工具调用格式**：采用 XML 风格的标签来格式化工具调用，确保工具使用的规范和解析的准确性。
- **对话管理**：提供对话管理功能，能够记录用户和助手的消息，并支持对话的清空操作。

## 安装与配置
### 依赖安装
确保你的 Python 版本 >= 3.11，然后使用以下命令安装项目依赖：
```bash
pip install -r requirements.txt
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

llm = OpenAIServer(api_key="", base_url="https://ark.cn-beijing.volces.com/api/v3", model_name="doubao-1-5-pro-32k-250115")
agent = Agent(llm=llm, tools=[Calculator()])

while True:
    query = input("请输入:")
    agent.generate(query)
    if query == "e":
        break
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
│   │   └── memory.py         # 记忆管理（目前为空）
│   └── tools/
│       ├── bocha.py          # Bocha 搜索工具
│       └── calculator.py     # 计算器工具
├── test.py                   # 测试脚本
├── pyproject.toml            # 项目依赖配置
└── .gitignore                # Git 忽略文件配置
```
