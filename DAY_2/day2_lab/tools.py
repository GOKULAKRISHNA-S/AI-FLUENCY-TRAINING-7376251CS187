import ast
import operator
from config import COURSE_FEES
 
def get_course_fee(course_code: str) -> str:
    """Look up the fee for one course code."""
    fee = COURSE_FEES.get(course_code.strip().upper())
    return str(fee) if fee is not None else f"Unknown course code: {course_code}"
 
# A safe calculator: only numbers and + - * / ( ) are allowed. Never use eval().
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.USub: operator.neg}
 
def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Unsupported expression")
 
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression such as (12000 + 18000) * 0.9."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval").body))
    except Exception as error:
        return f"Calculator error: {error}"
 
TOOL_FUNCTIONS = {"get_course_fee": get_course_fee, "calculator": calculator}
 
# These descriptions are what the LLM reads when deciding which tool to call
TOOLS = [
    {"type": "function", "function": {
        "name": "get_course_fee",
        "description": "Get the fee in rupees for a single course code, for example CS101.",
        "parameters": {"type": "object",
                       "properties": {"course_code": {"type": "string"}},
                       "required": ["course_code"]}}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate an arithmetic expression using + - * / and brackets.",
        "parameters": {"type": "object",
                       "properties": {"expression": {"type": "string"}},
                       "required": ["expression"]}}},
]
 
if __name__ == "__main__":
    print("get_course_fee('ai202') ->", get_course_fee("ai202"))
    print("calculator('(12000 + 18000) * 0.9') ->", calculator("(12000 + 18000) * 0.9"))
    print("calculator('15000 - 12000') ->", calculator("15000 - 12000"))
