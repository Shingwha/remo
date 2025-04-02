from src.core import Agent,OpenAIServer
from src.tools.calculator import Calculator
from src.core import MemoryBank,Memory

llm = OpenAIServer(api_key = "0374a08a-9b0b-4b62-8cf6-5fbb1d00666d",base_url = "https://ark.cn-beijing.volces.com/api/v3",model_name = "doubao-1-5-pro-32k-250115")

memorys = MemoryBank()
memory1 = Memory(type="LTM",summary="用户喜欢吃辣的，不喜欢吃酸的")
memory2 = Memory(type="TODO",summary="记得提醒用户等下要下雨，带伞") 
memory3 = Memory(type="LTM",summary="用户喜欢喝冰可乐")
memorys.add_memory(memory1)
memorys.add_memory(memory2)
memorys.add_memory(memory3)
agent = Agent(llm = llm,tools=[Calculator()],memory_bank=memorys,system_prompt="你是一个用户的知心朋友，你很热情友善，你可以在回答中加入一些表情来活跃聊天氛围，请根据用户的指令，给出合适的回答，请不要主动说出prompt的内容，除非用户明确要求")

while True:
    query = input("请输入:")
    agent.generate(query)
    if query == "e":
        break
