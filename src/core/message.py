from pydantic import BaseModel
from typing import List, Dict, Any


class Message(BaseModel):
    role: str
    content: str
    tool_call_id: str = None
    tool_call: str = None

    def __init__(self, role: str, content: str,**kwargs):
        super().__init__(role=role, content=content, **kwargs)

    def __str__(self):
        result = {"role": self.role, "content": self.content}
        if self.tool_call_id:
            result["tool_call_id"] = self.tool_call_id
        if self.tool_calls:
            result["tool_calls"] = self.tool_calls
        return result


class Conversation(BaseModel):
    messages: list[Message] = []

    def __str__(self):
        return [str(message) for message in self.messages]
    
    def __len__(self):
        return len(self.messages)
    
    def is_empty(self):
        return len(self.messages) == 0

    def add_message(self, message: Message) -> None:
        self.messages.append(message)

    def add_system_message(self, content: str) -> None:
        self.add_message(Message(role="system", content=content))

    def add_user_message(self, content: str) -> None:
        self.add_message(Message(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        self.add_message(Message(role="assistant", content=content))

    def add_tool_message(self, content: str, tool_calls: List[Dict[str, Any]]) -> None:
        self.add_message(
            Message(role="assistant", content=content, tool_calls=tool_calls)
        )

    def add_tool_result(self, content: str, tool_call_id: str) -> None:
        self.add_message(
            Message(role="tool", content=content, tool_call_id=tool_call_id)
        )

    def clear(self) -> None:
        self.messages = []
