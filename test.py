from src.core import Agent,OpenAIServer
from src.tools.calculator import Calculator
from src.tools.bocha import BochaSearch

llm = OpenAIServer(api_key = "",base_url = "https://ark.cn-beijing.volces.com/api/v3",model_name = "doubao-1-5-pro-32k-250115")
agent = Agent(llm = llm,tools = [Calculator()])
while True:
    query = input("请输入:")
    agent.generate(query)
    if query == "e":
        break
