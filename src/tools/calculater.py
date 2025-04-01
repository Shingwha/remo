from ..core.tool import Tool
import re


class Calculator(Tool):
    
    def __init__(self):
        self.name: str = "calculator"
        self.description: str= "A calculator that can perform basic arithmetic operations."
        self.parameters:list = [
        {
            "name": "expression", 
            "type": "string", 
            "required": True,
            "description": "The mathematical expression to evaluate (e.g. '2 + 3 * 4')"
        }
    ]
        self.usage:str = '''
<calculator>
<expression>2 + 3 * 4</expression>
</calculator>
'''
        self.func = self.calculate_expression

    def calculate_expression(self, args):
        """计算数学表达式的函数"""
        expr = args.get('expression')
        if not expr:
            return "Error: Missing expression parameter"
        
        # 安全检查：只允许基本数学运算和数字
        if not re.match(r'^[\d+\-*/().\s]+$', expr):
            return "Error: Invalid characters in expression"
            
        try:
            return str(eval(expr))
        except Exception as e:
            return f"Error: {str(e)}"
