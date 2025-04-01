
def parse_response(response):
    """解析LLM响应中的工具调用
    
    Args:
        response: LLM生成的响应文本，可能包含XML格式的工具调用
        
    Returns:
        List[Dict]: 工具调用列表，每个元素包含'tool'和'args'字段
        如果没有工具调用则返回None
    """
    import re
    from xml.etree import ElementTree as ET
    
    # 匹配XML格式的工具调用
    tool_pattern = r'<(\w+)>(.*?)</\1>'
    matches = re.findall(tool_pattern, response, re.DOTALL)
    
    if not matches:
        return None
        
    tool_calls = []
    for tool_name, tool_content in matches:
        try:
            # 解析工具参数
            root = ET.fromstring(f"<root>{tool_content}</root>")
            args = {}
            for child in root:
                args[child.tag] = child.text
                
            tool_calls.append({
                'tool': tool_name,
                'args': args
            })
        except ET.ParseError:
            continue
            
    return tool_calls if tool_calls else None
