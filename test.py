from src.core import Agent,OpenAIServer
from src.tools.calculater import Calculator


llm = OpenAIServer(api_key = "sk-d36f02bd49e64e08becd9c20e5fa7f58",base_url = "https://api.deepseek.com",model_name = "deepseek-chat")
agent = Agent(llm = llm,tools = [Calculator()])
agent.generate("帮我计算一下8888*7777和8888/7755")
