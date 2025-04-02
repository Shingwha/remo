from typing import List, Union,Callable
from dataclasses import dataclass, field
from .llm import BaseLLM
from .message import Conversation
from .tool import Tool, execute_tools
from .utils import parse_response
from .prompt import ToolsPrompt,SystemPrompt,MemoriesPrompt,QueryPrompt
from .memory import MemoryBank

@dataclass
class Agent():
    llm: BaseLLM
    tools: List[Union[Tool, Callable]] = field(default_factory=list)
    system_prompt: SystemPrompt = None
    conversation: Conversation = field(default_factory=Conversation)
    memory_bank: MemoryBank = None

    
    def _generate_prompts(self, query: str = None):
        prompt_list = []
        if self.conversation.is_empty():
            if self.system_prompt:
                prompt_list.append(SystemPrompt(self.system_prompt))
            if query:
                prompt_list.append(QueryPrompt(query))
            if self.tools:
                prompt_list.append(ToolsPrompt(tools=self.tools))
            if self.memory_bank:
                prompt_list.append(MemoriesPrompt(memory_bank=self.memory_bank))
        else:
            if query:
                prompt_list.append(QueryPrompt(query=query))
        prompt_content = ''
        for prompt in prompt_list:
            prompt_content += str(prompt)
        return prompt_content

    def generate(self, query: str = None):
        content = self._generate_prompts(query)
        self.conversation.add_user_message(content)
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
