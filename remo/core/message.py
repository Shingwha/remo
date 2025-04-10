from dataclasses import dataclass, field



@dataclass
class Message():
    role: str
    content: str

    def to_dict(self):
        return {"role": self.role, "content": self.content}

@dataclass
class Conversation():
    messages: list[Message] = field(default_factory=list)


    def __len__(self):
        return len(self.messages)
    
    def is_empty(self):
        return len(self.messages) == 0
    
    def to_dict(self):
        return [message.to_dict() for message in self.messages]

    def add_message(self, message: Message) -> None:
        self.messages.append(message)

    def add_user_message(self, content: str) -> None:
        self.add_message(Message(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        self.add_message(Message(role="assistant", content=content))

    def clear(self) -> None:
        self.messages = []
