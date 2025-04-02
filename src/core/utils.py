
def parse_response(response):
    """解析包含工具调用和内存操作的响应"""
    import re
    from xml.etree import ElementTree as ET
    
    # 匹配XML格式的操作标签
    action_pattern = r'<(\w+)>(.*?)</\1>'
    matches = re.findall(action_pattern, response, re.DOTALL)
    
    if not matches:
        return None
        
    tool_calls = []
    memory_actions = []
    
    for action_name, action_content in matches:
        try:
            # 修复XML格式问题 - 确保内容被正确包裹
            xml_content = f"<root>{action_content.strip()}</root>"
            root = ET.fromstring(xml_content)
            
            args = {}
            for child in root:
                args[child.tag] = child.text.strip() if child.text else ""
                
            if 'memory' in action_name.lower():
                memory_actions.append({
                    'action': action_name,
                    'args': args
                })
            else:
                tool_calls.append({
                    "tool": action_name,
                    "args": args
                })
                
        except ET.ParseError as e:
            print(f"XML解析错误: {e}")
            continue
            
    return {
        'tool_calls': tool_calls if tool_calls else None,
        'memory_actions': memory_actions if memory_actions else None
    }
