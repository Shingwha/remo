from dataclasses import dataclass

@dataclass
class BasePrompt():
    name: str = None
    description: str = None
    content: str = None

    def __str__(self):
        return f"""
====
{self.name if self.name else ""}
{self.description if self.description else ""}
{self.content if self.content else ""} 
====
"""

class SystemPrompt(BasePrompt):
    name: str = "SYSTEM PROMPT"



class ToolUsePrompt(BasePrompt):
    
    def __init__(self):
        self.name: str = "TOOL USE"
        self.description: str = "When you are unsure about certain information or need to perform specific actions, you can use the tools according to the following requirements."
        self.content: str = '''
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
    def __init__(self,tool):
        self.tool = tool
        self.name = self.tool.name
        self.description = self.tool.description
        self.parameters = self.parse_tool_parameters()
        self.usage = self.tool.usage

    def parse_tool_parameters(self):
        params_str = []
        for param in self.tool.parameters:
            required = "(required)" if param.get('required', False) else "(optional)"
            param_desc = param.get('description', '')
            params_str.append(f"- {param['name']}:{required} {param_desc}")
        return "\n".join(params_str)

    def __str__(self):
        return f"""
## {self.name}
Description: {self.description}
Parameters: {self.parameters}
Usage: {self.usage}
"""

class ToolsPrompt(BasePrompt):
    name: str = "Tools"
    def __init__(self,tools):
        self.tool_use_prompt = ToolUsePrompt()
        self.tools = tools

    def __str__(self):
        tools_str = "\n".join(str(ToolPrompt(tool)) for tool in self.tools)
        return f"""
{str(self.tool_use_prompt)}
# {self.name}
{tools_str}
"""

if __name__ == "__main__":
    print(ToolsPrompt([]))