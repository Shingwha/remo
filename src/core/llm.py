from pydantic import BaseModel
from typing import List
from openai import OpenAI
from .message import Conversation
from typing import Dict, Any, Union


class BaseLLM(BaseModel):
    api_key: str
    base_url: str
    model_name: str
    stream: bool = False
    temperature: float = None
    max_tokens: int = None
    top_p: float = None
    frequency_penalty: float = None
    client = None

    def __init__(self, **data):
        super().__init__(**data)


class OpenAIServer(BaseLLM):
    def __init__(self, **data):
        super().__init__(**data)

    def generate(
        self,
        messages: Union[List[Dict[str, Any]], Conversation],
    ) -> Dict[str, Any]:
        kwargs = {
            "model": self.model_name,
            "messages": messages,
        }
        if self.temperature:
            kwargs["temperature"] = self.temperature
        if self.max_tokens:
            kwargs["max_tokens"] = self.max_tokens

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message
