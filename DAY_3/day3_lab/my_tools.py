"""Day 3: tools for the agent you build yourself."""
import ast
import operator
import os
import re

# ---------- Tool 1: a safe calculator ----------
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg}

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
        return f"Calculator error: {error}. Use only numbers and + - * / ( )."

# ---------- Tool 2: a web page reader ----------
TAG = re.compile(r"<(script|style)[^>]*>.*?</\1>|<[^>]+>", re.S | re.I)
SPACES = re.compile(r"\s+")

def read_webpage(url: str, max_chars: int = 2000) -> str:
    """Fetch a web page (http/https) or a local .html/.txt file and return its text."""
    try:
        if url.startswith("http://") or url.startswith("https://"):
            import requests
            response = requests.get(url, timeout=10,
                                    headers={"User-Agent": "AgenticAI-Lab/1.0"})
            response.raise_for_status()
            raw = response.text
        elif os.path.exists(url):
            raw = open(url, encoding="utf-8", errors="ignore").read()
        else:
            return f"Read error: '{url}' is not a URL and no such file exists."
    except Exception as error:
        return f"Read error: {type(error).__name__}: {error}"

    text = SPACES.sub(" ", TAG.sub(" ", raw)).strip()
    if len(text) > max_chars:                      # guard against context overflow
        text = text[:max_chars] + f" ... [truncated, {len(text)} characters total]"
    return text or "Read error: the page contained no readable text."

TOOL_FUNCTIONS = {"calculator": calculator, "read_webpage": read_webpage}

TOOLS = [
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate an arithmetic expression using + - * / ** and brackets, "
                       "for example (12000 + 18000) * 0.9.",
        "parameters": {"type": "object",
                       "properties": {"expression": {"type": "string",
                                      "description": "The arithmetic expression to evaluate"}},
                       "required": ["expression"]}}},
    {"type": "function", "function": {
        "name": "read_webpage",
        "description": "Read a web page or a local HTML/text file and return its visible text. "
                       "Give a full URL such as https://example.com or a file name such as notice.html.",
        "parameters": {"type": "object",
                       "properties": {"url": {"type": "string",
                                      "description": "URL or local file name to read"}},
                       "required": ["url"]}}},
]

if __name__ == "__main__":
    print(calculator("(12000 + 18000) * 0.9"))
    print(calculator("2 ** 10"))
    print(calculator("import os"))
    print(read_webpage("notice.html")[:200])
    print(read_webpage("no_such_file.html"))