# Remo 

## 项目概述
Remo 是一个基于大语言模型的小型 Agent 框架



```python
from remo.core import Agent, OpenAIServer, MemoryBank
from remo.tools import Calculator, ZhiPuWebSearch

### Web 交互界面
```bash
python gradio_ui.py
```
启动后访问 `http://127.0.0.1:7860` 使用可视化界面


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


