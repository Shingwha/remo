from dataclasses import dataclass
import datetime

@dataclass
class BasePrompt():
    name: str = None
    description: str = None
    content: str = None

    def __str__(self):
        return f"====\n{self.name or ''}\n{self.description or ''}\n{self.content}\n" if self.content else None


class SystemPrompt(BasePrompt):
    
    def __init__(self,content):
        self.name: str = "SYSTEM_PROMPT"
        self.content: str = content

    def __str__(self):
        return f"====\n{self.name}\n{self.content}" if self.content else None

class QueryPrompt(BasePrompt):

    def __init__(self,content):
        self.name: str = "QUERY"
        self.description: str = "User's query is provided as following:"
        self.content: str = content


class ToolUsePrompt(BasePrompt):
    
    def __init__(self):
        self.name: str = "TOOL USE"
        self.description: str = """
When you are unsure about certain information or need to perform specific actions, you can use the tools according to the following requirements.
But if the query of user is not related to tools, please ignore the prompt of this section.
Please do not output tool use format you do not want to use a tool actually, or it will cause errors.
"""
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


class MemoryActionRulesPrompt(BasePrompt):
    
    def __init__(self):
        self.name: str = "MEMORY ACTION"
        self.description: str = f"""
When you need to manage memories (add, delete or search), you can use memory actions according to the following requirements.
Please remember current time is {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}.
Please do not output memory action format you do not want to use actually, or it will cause errors.
"""
        self.content: str = '''
# Memory Actions Formatting

Memory actions are formatted using XML-style tags similar to tool use. Here's the structure:
"""
<action_name>
<arg1_name>value1</arg1_name>
<arg2_name>value2</arg2_name>
<action_name>
"""
You can output multiple memory actions if needed:
"""
<action1>
<arg1_name>value1</arg1_name>
<arg2_name>value2</arg2_name>
<action1>
"""
<action2>
<arg1_name>value1</arg1_name>
<arg2_name>value2</arg2_name>
<action2>
"""
'''


class MemoryActionsPrompt(BasePrompt):
    def __init__(self):
        self.name = "Memory Actions"
        self.description = "Available memory actions:"
        self.content = """
## add_memory_by_args
Description: if you or User want to add a memory,or if User want you to memorize something, you can use this tool to add a memory
Add only what you'll truly need later—future tasks, key info, or meaningful reminders.
Parameters:
- summary: (required) Summary text of the memory
- type: (required) Memory type (USER/SYSTEM/TODO). 
    - USER: For personal user information, preferences, and facts
    - SYSTEM: For your own information, preferences, and facts
    - TODO: For tasks and reminders
- keywords: (optional) List of keywords
- time: (optional) Time of reminded ,format: YYYY-MM-DDTHH:MM, if not provided, the time must not be current time
- status: (optional) Status of the memory,you can set anything you want, eg.if you want to remind user a TODO, you can set status to "待提醒用户"

## delete_memory_by_id
Description: if you or User want to delete a memory, you can use this tool
Parameters: 
- id: (required) Memory ID to delete

## search_memory_by_id
Description: if you or User want to get more information about a memory, you can use this tool
Parameters:
- id: (required) Memory ID to search

## update_memory_by_id
Description: if User want to update a memory or you have a wrong memory, you can use this tool
Parameters:
- id: (required) Memory ID to update
- summary: (optional) New summary text of the memory
- type: (optional) New memory type (USER/SYSTEM/TODO)
- keywords: (optional) New list of keywords
- time: (optional) New time of reminded, format: YYYY-MM-DDTHH:MM, if not provided, the time must not be current time
- status: (optional) New status of the memory,you can set anything you want, eg. "已提醒用户但还不知道是否完成" or "已提醒用户这件事并且用户已完成"
"""


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
        self.description = "The tools you have access to:"
        self.tools = tools

    def __str__(self):
        tools_str = "".join(str(ToolPrompt(tool)) for tool in self.tools)
        return f"""
{str(self.tool_use_prompt)}
# {self.name}
{self.description}
{tools_str}
"""


class MemoryPrompt(BasePrompt):
    def __init__(self, memory):
        self.memory = memory
        self.name = f"Memory: {self.memory.type}"
        self.summary = self.memory.summary
        self.id = self.memory.id
        self.time = self.memory.time or ""
        self.status = self.memory.status or ""
        self.keywords = self.memory.keywords or ""

    def __str__(self):
        return f"""
## {self.name}
ID: {self.id}
Summary: {self.summary}
Keywords: {self.keywords}
Time: {self.time}
Status: {self.status}
"""


class MemoriesPrompt(BasePrompt):
    name: str = "Memories"
    def __init__(self, memory_bank):
        self.description = "Please remember SYSTEM is youself,Relevant memories:"
        self.memory_bank = memory_bank
        self.memory_action_prompt = MemoryActionRulesPrompt()
        self.memory_actions_prompt = MemoryActionsPrompt()

    def __str__(self):
        memories_str = "".join(str(MemoryPrompt(mem)) for mem in self.memory_bank)
        return f"""
====
{str(self.memory_action_prompt)}
{str(self.memory_actions_prompt)}
# {self.name}
{self.description}
{memories_str}
"""


def generate_prompts(query: str = None, tools=None, memory_bank=None, system_prompt=None) -> str:
        prompt_list = []
        if system_prompt:
            prompt_list.append(SystemPrompt(system_prompt))
        if query:
            prompt_list.append(QueryPrompt(query))
        if tools:
            prompt_list.append(ToolsPrompt(tools=tools))
        if memory_bank:
            prompt_list.append(MemoriesPrompt(memory_bank=memory_bank))
        prompt_content = ''
        for prompt in prompt_list:
            prompt_content += str(prompt)
        return prompt_content
