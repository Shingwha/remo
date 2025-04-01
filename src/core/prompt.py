from pydantic import BaseModel

class BasePrompt(BaseModel):
    name: str
    description: str
    content: str

    def __init__(self, **data):
        super().__init__(**data)

    def __str__(self):
        return f"""
====
{self.name}
{self.description}
{self.content}
====
"""

class ToolUsePrompt(BasePrompt):
    name: str = "TOOL USE"
    description: str = "When you are unsure about certain information or need to perform specific actions, you can use the tools according to the following requirements."
    content: str = '''
# Tool Use Formatting

Tool use is formatted using XML-style tags. The tool name is enclosed in opening and closing tags, and each parameter is similarly enclosed within its own set of tags. Here's the structure:
"""
<tool_name>
<parameter1_name>value1</parameter1_name>
<parameter2_name>value2</parameter2_name>
...
</tool_name>
"""
For example:
"""
<read_file>
<path>src/main.js</path>
</read_file>
"""
Always adhere to this format for the tool use to ensure proper parsing and execution.
If you want to use multiple tools, you can directly output the structured parameters of multiple tools:
"""
<tool_name1>
<parameter1_name>value1</parameter1_name>
<parameter2_name>value2</parameter2_name>
<tool_name1>
"""
"""
<tool_name2>
<parameter1_name>value1</parameter1_name>
<parameter2_name>value2</parameter2_name>
<tool_name2>
"""
'''

class ToolPrompt(BasePrompt):
    name: str = "TOOL"
    description: str
    parameters: list
    usage: str

    def __init__(self, **data):
        super().__init__(**data)

    def __str__(self):
        return f"""
## {self.name}
Description: {self.description}
Parameters: {self.parameters}
Usage: {self.usage}
"""

class ToolsPrompt(BasePrompt):
    name: str = "Tools"
    tools: list

    def __init__(self, **data):
        super().__init__(**data)

    def __str__(self):
        tools_str = "\n".join(str(tool) for tool in self.tools)
        return f"""
# {self.name}
{tools_str}
"""
