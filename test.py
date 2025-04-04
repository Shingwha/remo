from src.core import Agent,OpenAIServer
from src.core import MemoryBank
from dotenv import load_dotenv
import os 


load_dotenv()  

api_key = os.environ.get("OPENAI_API_KEY")
llm = OpenAIServer(api_key = api_key,base_url = "https://ark.cn-beijing.volces.com/api/v3",model_name = "deepseek-v3-250324")

memorys = MemoryBank(storage_path="my_memory.json")
agent = Agent(llm = llm,memory_bank=memorys,system_prompt="你是阿华的好朋友阿江，同时你擅长使用记忆工具，但请注意：不是所有的对话都需要被记住，只需要记住关于用户或自己的重要的身份认同的信息，日常简单对话不需要记下，比如打招呼、简单问答之类的")

if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input == "exit":
            print("Goodbye!")
            break
        elif user_input == "clear":
            agent.conversation.clear()
            print("Conversation cleared.")
        elif user_input == "context":
            print("Context:", str(agent.conversation))
        else:
            result = agent.generate(user_input)
            print("Agent:",result)

