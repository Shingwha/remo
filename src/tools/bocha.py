from ..core.tool import Tool
import requests
import json
from datetime import datetime


class BochaSearch(Tool):

    def __init__(self,api_key:str):
        self.api_key = api_key
        self.name = "bocha_search"
        self.description = "Search news and information from Bocha_search_tool"
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
        self.func = self.bocha_search


    def bocha_search(self, query):
        url = "https://api.bochaai.com/v1/web-search"
        payload = json.dumps(
            {
                "query": query,
                "freshness": "noLimit",
                "summary": True,
                "count": 20,
            }
        )
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        raw_data = response.json()

        if raw_data.get("code") == 200:
            filtered_results = []
            formatted_results = []
            # 直接访问 webPages.value 数组
            for item in raw_data.get("data", {}).get("webPages", {}).get("value", []):
                # 处理日期格式
                date_str = item.get("dateLastCrawled")
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                except (ValueError, TypeError):
                    date = None

                filtered = {
                    "name": item.get("name"),
                    "url": item.get("url"),
                    "snippet": item.get("snippet"),
                    "summary": item.get("summary"),
                    "dateLastCrawled": date,
                }
                filtered_results.append(filtered)

            # 按日期倒序排列
            filtered_results.sort(key=lambda x: x["dateLastCrawled"], reverse=True)

            # 格式化每条新闻信息
            for idx, item in enumerate(filtered_results, start=1):
                formatted = (
                    f"新闻 {idx}:\n"
                    f"标题: {item['name']}\n"
                    f"链接: {item['url']}\n"
                    f"摘要: {item['snippet']}\n"
                    f"总结: {item['summary']}\n"
                    f"时间: {item['dateLastCrawled'].strftime('%Y-%m-%d %H:%M:%S') if item['dateLastCrawled'] else '未知'}"
                )
                formatted_results.append(formatted)

            return formatted_results
        else:
            return raw_data
