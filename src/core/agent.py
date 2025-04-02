from typing import List, Union,Callable
from dataclasses import dataclass, field
from .llm import BaseLLM
from .message import Conversation
from .tool import Tool, execute_tools
from .utils import parse_response
from .prompt import ToolsPrompt,SystemPrompt,MemoryPrompt
from .memory import MemoryBank

@dataclass
class Agent():
    llm: BaseLLM
    tools: List[Union[Tool, Callable]] = field(default_factory=list)
    system_prompt: SystemPrompt = None
    content_prompt: str = None
    tools_prompt: ToolsPrompt = None
    conversation: Conversation = field(default_factory=Conversation)
    memory_bank: MemoryBank = None
    memory_prompt: MemoryPrompt = None

    def generate(self,query:str = None):
        if self.conversation.is_empty():
            if self.tools:
                self.tools_prompt = ToolsPrompt(tools = self.tools)
            if self.memory_bank:
                self.memory_prompt = MemoryPrompt(memory_bank = self.memory_bank)
            for prompt in [self.system_prompt,self.tools_prompt,self.memory_prompt,self.content_prompt]:
                if prompt:
                    query += str(prompt)
        self.conversation.add_user_message(query)
        while True:
            response = self.llm.generate(self.conversation.to_dict())
            content = response.content
            self.conversation.add_assistant_message(content)
            tool_calls = parse_response(content)
            if tool_calls:
                results = execute_tools(tool_calls, self.tools)
                self.conversation.add_user_message(str(results))
            else:
                break

        return content
