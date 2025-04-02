from typing import List, Union,Callable
from dataclasses import dataclass, field
from .llm import BaseLLM
from .message import Conversation
from .tool import Tool, execute_tools
from .utils import parse_response
from .prompt import generate_prompts
from .memory import MemoryBank, execute_memory_actions

@dataclass
class Agent():
    llm: BaseLLM
    tools: List[Union[Tool, Callable]] = field(default_factory=list)
    system_prompt: str = None
    conversation: Conversation = field(default_factory=Conversation)
    memory_bank: MemoryBank = None

    def generate(self, query: str = None):
        print(f"Query: {query}")
        if self.conversation.is_empty():
            content = generate_prompts(
                query=query,
                system_prompt=self.system_prompt,
                tools=self.tools,
                memory_bank=self.memory_bank)
        else:
            content = query
        
        self.conversation.add_user_message(content)
        while True:
            response = self.llm.generate(self.conversation.to_dict())
            content = response.content
            print(f"Assistant: {content}")
            self.conversation.add_assistant_message(content)
            parsed_response = parse_response(content)
            if parsed_response:
                results = []
                if parsed_response['tool_calls']:
                    results.append(execute_tools(parsed_response['tool_calls'], self.tools))
                if parsed_response['memory_actions']:
                    results.append(execute_memory_actions( self.memory_bank,parsed_response['memory_actions']))
                self.conversation.add_user_message(str(results))
            else:
                break

        return content
