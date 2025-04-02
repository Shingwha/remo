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
        content = generate_prompts(
            query=query,
            conversation=self.conversation,
            system_prompt=self.system_prompt,
            tools=self.tools,
            memory_bank=self.memory_bank)
        self.conversation.add_user_message(content)
        while True:
            response = self.llm.generate(self.conversation.to_dict())
            content = response.content
            self.conversation.add_assistant_message(content)
            parsed_response = parse_response(content)
            if parsed_response:
                if parsed_response['tool_calls']:
                    results = execute_tools(parsed_response['tool_calls'], self.tools)
                    self.conversation.add_user_message(str(results))
                elif parsed_response['memory_actions'] and self.memory_bank:
                        execute_memory_actions(parsed_response['memory_actions'], self.memory_bank)
                else:
                    break
            else:
                break

        return content
