from remo.core import Agent,OpenAIServer
from remo.core import MemoryBank
from dotenv import load_dotenv
import os 
from remo.tools import ZhiPuWebSearch,BochaWebSearch



load_dotenv()  
deepseek_chat = "deepseek-v3-250324"
deepseek_r1 = "deepseek-r1-250120"
deepseek_7b = "deepseek-r1-distill-qwen-7b-250120"
deepseek_32b = "deepseek-r1-distill-qwen-32b-250120"
llm_api_key = os.environ.get("DOUBAO_API_KEY")
llm = OpenAIServer(api_key = llm_api_key,base_url = "https://ark.cn-beijing.volces.com/api/v3",model_name = deepseek_chat)
zhipu_api_key = os.environ.get("ZHIPU_API_KEY")
zhipu_web_search = ZhiPuWebSearch(api_key=zhipu_api_key)
bocha_api_key = os.environ.get("BOCHA_API_KEY")
bocha_web_search = BochaWebSearch(api_key=bocha_api_key)

memorys = MemoryBank(storage_path="my_memory.json")
agent = Agent(llm = llm,memory_bank=memorys,tools=[zhipu_web_search],system_prompt="你是阿华的好朋友阿江")


def main():
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

if __name__ == "__main__":
    
    main()
    

