from pydantic import BaseModel
from typing import List,Callable,Dict

class Tool(BaseModel):
    name: str
    description: str = ""
    parameters: List[Dict] = []  
    # parameters: List[Dict] = [{'name': 'param1', 'required': True, 'description': 'description of param1'}, {'name': 'param2', 'required': False,'description': 'description of param2'}]
    usage: str = "" 
    """
    <read_file>
    <path>File path here</path>
    </read_file>"
    """
    func: Callable

    def execute(self, args):
        return self.func(args)








def execute_tools(tool_calls,tools):
    tools_dict = {tool.name: tool for tool in tools} if tools else {}
    results = {}
    for tool_call in tool_calls:
        tool_name = tool_call['tool']
        tool_args = tool_call['args']
        if tool_name in tools_dict:
            tool = tools_dict[tool_name]
            result = tool.execute(tool_args)
            results[tool_name] = result
        else:
            results[tool_name] = f"Tool <{tool_name}> not found"
    return results