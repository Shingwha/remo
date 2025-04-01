from pydantic import BaseModel
from typing import List, Dict,Optional,Union,Callable
from .llm import BaseLLM
from .message import Conversation
from .memory import MemoryBank
from .tool import Tool

class Agent(BaseModel):
    llm: BaseLLM
    tools: List[Union[Tool, Callable]]
    system_prompt: str = "你是一个智能代理，协调LLM和工具使用"
    content_prompt: str = None
    conversation: Conversation
    memorybank: MemoryBank

    def __init__(self, **data):
        super().__init__(**data)

    def generate(self,query:str = None):
        if self.conversation.is_empty():
            self.conversation.add_system_message(self.system_prompt)
            if self.content_prompt:
                query = self.content_prompt + query
        self.conversation.add_user_message(query)
        while True:
            response = self.llm.generate(str(self.conversation))
            pass