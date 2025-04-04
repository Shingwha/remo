from typing import List,Callable,Dict
from dataclasses import dataclass, field


@dataclass
class Tool():
    name: str
    func: Callable
    description: str = ""
    parameters: List[Dict] = field(default_factory=list)
    # parameters: List[Dict] = [{'name': 'param1', 'required': True, 'description': 'description of param1'}, {'name': 'param2', 'required': False,'description': 'description of param2'}]
    usage: str = "" 
    """
    <read_file>
    <path>File path here</path>
    </read_file>"
    """

    def execute(self, **args):
        return self.func(**args)


def execute_tools(tool_calls,tools):
    tools_dict = {tool.name: tool for tool in tools} if tools else {}
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call['tool']
        tool_args = tool_call['args']
        if tool_name in tools_dict:
            tool = tools_dict[tool_name]
            result = tool.execute(**tool_args)
            results.append({
                'tool': tool_name,
                'args': tool_args,
                'result': result
            })
        else:
            results.append({
                'tool': tool_name,
                'args': tool_args,
                'result': f"Tool <{tool_name}> not found"
            })
    return results
