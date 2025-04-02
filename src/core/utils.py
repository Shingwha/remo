
def parse_response(response):
    
    import re
    from xml.etree import ElementTree as ET
    
    action_pattern = r'<(\w+)>(.*?)</\1>'
    matches = re.findall(action_pattern, response, re.DOTALL)
    
    if not matches:
        return None
        
    tool_calls = []
    memory_calls = []
    
    for action_name, action_content in matches:
        try:
            root = ET.fromstring(f"<root>{action_content}</root>")
            args = {}
            for child in root:
                args[child.tag] = child.text
            if 'memory' in action_name.lower():
                memory_action = {
                    'action': action_name,
                    'args': args
                }
                memory_calls.append(memory_action)
            else:
                tool_call = {
                    "tool": action_name,
                    "args": args
                }
                tool_calls.append(tool_call)
                
        except ET.ParseError:
            continue
            
    return {
        'tool_calls': tool_calls if tool_calls else None,
        'memory_actions': memory_calls if memory_calls else None
    }
