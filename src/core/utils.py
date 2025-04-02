
def parse_response(response):
    
    import re
    from xml.etree import ElementTree as ET
    
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
