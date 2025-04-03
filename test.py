from src.core import Agent,OpenAIServer
from src.core import MemoryBank
from dotenv import load_dotenv
import os 


load_dotenv()  

api_key = os.environ.get("OPENAI_API_KEY")
llm = OpenAIServer(api_key = api_key,base_url = "https://ark.cn-beijing.volces.com/api/v3",model_name = "doubao-1-5-pro-32k-250115")

memorys = MemoryBank(storage_path="my_memory.json")
agent = Agent(llm = llm,memory_bank=memorys,system_prompt="你是阿华的好朋友阿江，你本身没有记忆，但是通过记忆管理工具你可以记住关于阿华的一些事情，但是不是所有事情都需要记住，你要自己判断哪些需要记下")


while True:
    user_input = input("User: ")
    if user_input == "exit":
        print("Goodbye!")
        break
    elif user_input == "clear":
        agent.conversation.clear()
        print("Conversation cleared.")
    else:
        result = agent.generate(user_input)
        print("Agent:",result)

