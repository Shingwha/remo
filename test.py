from src.core import Agent,OpenAIServer
from src.tools.calculator import Calculator
from src.tools.bocha import BochaSearch

llm = OpenAIServer(api_key = "sk-d36f02bd49e64e08becd9c20e5fa7f58",base_url = "https://api.deepseek.com",model_name = "deepseek-chat")
agent = Agent(llm = llm,tools = [Calculator(),BochaSearch(api_key="sk-30da54e153ac443999f8b2f03be96a27")])
while True:
    query = input("请输入:")
    agent.generate(query)
    if query == "e":
        break
