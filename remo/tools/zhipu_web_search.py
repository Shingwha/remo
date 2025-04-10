from ..core.tool import Tool
import requests
import uuid

class ZhiPuWebSearch(Tool):
    
    def __init__(self,api_key):
        self.name: str = "zhipu_web_search"
        self.description: str = "使用智谱AI的web搜索API进行网络搜索"
        self.parameters: list = [
            {
                "name": "query", 
                "type": "string", 
                "required": True,
                "description": "搜索查询内容"
            }
        ]
        self.usage: str = '''
<zhipu_web_search>
<query>搜索内容</query>
</zhipu_web_search>
'''
        self.api_key = api_key
        self.func = self.web_search


    def web_search(self, query):
        msg = [
        {
            "role": "user",
            "content":query
        }
    ]
        tool = "web-search-pro"
        url = "https://open.bigmodel.cn/api/paas/v4/tools"
        request_id = str(uuid.uuid4())
        data = {
            "request_id": request_id,
            "tool": tool,
            "stream": False,
            "messages": msg
        }

        resp = requests.post(
            url,
            json=data,
            headers={'Authorization': self.api_key},
            timeout=300
        )
        result = resp.json()
        simplified_results = []
        if "choices" in result and len(result["choices"]) > 0:
            for item in result["choices"][0]["message"]["tool_calls"][1]["search_result"]:
                simplified_results.append({
                    "title": item.get("title", ""),
                    "content": item.get("content", ""),
                    "media": item.get("media", "")
                })
        return simplified_results
