from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


    def __init__(self, role: str, content: str,**kwargs):
        super().__init__(role=role, content=content, **kwargs)

    def __str__(self):
        return {"role": self.role, "content": self.content}


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

    def add_user_message(self, content: str) -> None:
        self.add_message(Message(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        self.add_message(Message(role="assistant", content=content))

    def clear(self) -> None:
        self.messages = []
