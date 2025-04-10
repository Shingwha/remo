from ..core.tool import Tool
import requests


class BochaWebSearch(Tool):

    def __init__(self,api_key:str):
        self.api_key:str = api_key
        self.name:str = "bocha_search"
        self.description:str = "Search news and information from this tool"
        self.parameters:list = [
            {
                "name": "query",
                "type": "string",
                "required": True,
                "description": "The search query for Bocha",
            } 
        ]
        self.usage:str = """
<bocha_search>
<query>something you want to search</query>
</bocha_search>
        """
        self.func = self.bocha_web_search   


    def bocha_web_search(self, query:str):

        url = "https://api.bochaai.com/v1/web-search"
        payload = {
            "query": query,
            "summary": True,
            "count": 20,
            "page": 1
        }
        Bearer_api_key = "Bearer "+self.api_key
        headers = {
        'Authorization': Bearer_api_key,
        'Content-Type': 'application/json'
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
