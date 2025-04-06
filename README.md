# Remo - 智能对话助手框架

## 项目概述
Remo 是一个基于大语言模型的智能 Agent 框架，专注于提供流畅的对话体验和强大的工具扩展能力。通过模块化设计，开发者可以轻松集成各种工具并管理对话上下文，构建个性化的智能助手。

## 核心优势

- **开箱即用**：提供完整的对话管理和工具调用框架
- **灵活扩展**：支持快速添加自定义工具
- **记忆持久化**：对话记忆可本地存储和检索
- **多接口支持**：同时提供命令行和 Web 交互界面

## 快速开始

### 安装依赖
```bash
uv pip install .
```

### 基本配置
1. 创建 `.env` 文件配置 API 密钥：
```env
DOUBAO_API_KEY=your_api_key_here
ZHIPU_API_KEY=your_zhipu_key_here
BOCHA_API_KEY=your_bocha_key_here
```

2. 初始化 Agent：
```python
from src.core import Agent, OpenAIServer, MemoryBank
from src.tools import Calculator, ZhiPuWebSearch

# 配置 LLM 服务
llm = OpenAIServer(
    api_key=os.getenv("DOUBAO_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    model_name="deepseek-v3-250324"
)

# 初始化工具和记忆
tools = [Calculator(), ZhiPuWebSearch(api_key=os.getenv("ZHIPU_API_KEY"))]
memory = MemoryBank(storage_path="memory.json")

# 创建个性化助手
agent = Agent(
    llm=llm,
    tools=tools,
    memory_bank=memory,
    system_prompt="你是一个贴心的助手，善于使用工具解决问题"
)
```

## 使用方式

### 命令行交互
```bash
python test.py
```
支持命令：
- `exit` - 退出程序
- `clear` - 清空对话历史
- `context` - 查看当前对话上下文

### Web 交互界面
```bash
python gradio_ui.py
```
启动后访问 `http://127.0.0.1:7860` 使用可视化界面

## 核心功能

### 工具系统
- **内置工具**：
  - `Calculator`：数学计算
  - `ZhiPuWebSearch`：智谱网络搜索
  - `BochaWebSearch`：Bocha 信息检索

- **自定义工具**：
  继承 `Tool` 基类并实现：
  ```python
  class MyTool(Tool):
      def __init__(self):
          self.name = "my_tool"
          self.description = "工具描述"
          self.parameters = [{"name": "param", "description": "参数说明"}]
          self.func = self.execute
      
      def execute(self, **args):
          return "执行结果"
  ```

### 记忆管理
支持四种记忆操作：
```xml
<add_memory_by_args>
<summary>重要事项</summary>
<type>TODO</type>
</add_memory_by_args>

<search_memory_by_id>
<id>MEMORY_ID</id>
</search_memory_by_id>
```

## 项目结构
```
src/
├── core/               # 核心模块
│   ├── agent.py        # Agent 主逻辑
│   ├── llm.py          # LLM 接口
│   ├── memory.py       # 记忆系统
│   └── tool.py         # 工具基类
├── tools/              # 工具实现
│   ├── calculator.py   # 计算器
│   └── web_search/     # 搜索工具
gradio_ui.py            # Web 界面
test.py                 # 命令行入口
```

## 开发指南

1. **添加新工具**：
   - 在 `src/tools/` 下创建工具类
   - 在 `__init__.py` 中导出
   - 更新 Agent 的 tools 参数

2. **修改提示模板**：
   编辑 `src/core/prompt.py` 中的提示类

3. **扩展记忆类型**：
   修改 `Memory` 类的 `type` 字段约束

## 最佳实践

- 为每个工具编写清晰的参数说明
- 使用枚举类型约束工具参数
- 为重要记忆添加时间戳
- 定期清理无用记忆

## 常见问题

**Q：工具调用失败怎么办？**
A：检查工具参数是否符合 XML 格式要求，并确保所有必填参数已提供

**Q：记忆不更新？**
A：确认是否有存储路径写入权限，检查文件是否被其他进程占用

**Q：如何提高响应速度？**
A：减少不必要的工具调用，优化提示词长度
