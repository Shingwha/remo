from src.core import Agent,OpenAIServer
from src.tools.calculator import Calculator
from src.core import MemoryBank,Memory
import time

llm = OpenAIServer(api_key = "",base_url = "https://ark.cn-beijing.volces.com/api/v3",model_name = "doubao-1-5-pro-32k-250115")

memorys = MemoryBank(storage_path="my_memory.json")
agent = Agent(llm = llm,tools=[Calculator()],memory_bank=memorys,system_prompt="你是一个用户的知心朋友，你很热情友善，你可以在回答中加入一些表情来活跃聊天氛围，请根据用户的指令，给出合适的回答，请不要主动说出prompt的内容，除非用户明确要求")

while True:
    # 推迟0.5s
    time.sleep(0.2)
    query = input("请输入:")
    if query == "exit":
        break
    elif query == "clear":
        agent.conversation.clear()
    else:
        agent.generate(query)
    
