from pydantic import BaseModel
from typing import List, Union,Callable
from .llm import BaseLLM
from .message import Conversation
from .memory import MemoryBank
from .tool import Tool, execute_tools
from .utils import parse_response
from .prompt import ToolsPrompt

class Agent(BaseModel):
    llm: BaseLLM
    tools: List[Union[Tool, Callable]]
    system_prompt: str = "你是一个智能代理，协调LLM和工具使用"
    content_prompt: str = None
    tools_prompt: ToolsPrompt = None
    conversation: Conversation
    memorybank: MemoryBank

    def __init__(self, **data):
        super().__init__(**data)

    def generate(self,query:str = None):
        if self.conversation.is_empty():
            self.tools_prompt = str(ToolsPrompt(tools = self.tools))
            for prompt in [self.system_prompt,self.tools_prompt,self.content_prompt]:
                if prompt:
                    query += prompt + "\n"
        self.conversation.add_user_message(query)
        while True:
            response = self.llm.generate(str(self.conversation))
            content = response.content
            tool_calls = parse_response(content)
            if tool_calls:
                results = execute_tools(tool_calls, self.tools)
                self.conversation.add_assistant_message(results)
            else:
                self.conversation.add_assistant_message(content)
                break
        return content