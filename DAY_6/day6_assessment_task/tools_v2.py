import ast
import operator

ITEM_PRICES = {
    "projector": 2500,
    "microphone": 1200,
    "chair": 80,
    "table": 250,
    "banner": 600,
    "certificate": 40,
    "notebook": 120,
    "pen": 20
}

VENUE_CHARGES = {
    "classroom": 1000,
    "seminar_hall": 3000,
    "auditorium": 7000
}

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg
}

def get_item_price(item: str, category: str = "equipment") -> str:
    item = item.strip().lower()
    price = ITEM_PRICES.get(item)

    if price is None:
        return f"Unknown item: {item}. Valid items: {', '.join(ITEM_PRICES)}"

    return str(price)

def get_venue_charge(venue_type: str) -> str:
    venue_type = venue_type.strip().lower()
    charge = VENUE_CHARGES.get(venue_type)

    if charge is None:
        return f"Unknown venue: {venue_type}. Valid venues: {', '.join(VENUE_CHARGES)}"

    return str(charge)

def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](
            _evaluate(node.left),
            _evaluate(node.right)
        )

    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](
            _evaluate(node.operand)
        )

    raise ValueError("Unsupported expression")

def calculate_event_cost(expression: str) -> str:
    try:
        result = _evaluate(ast.parse(expression, mode="eval").body)
        return str(result)
    except Exception as error:
        return f"Calculation error: {error}. Use only numbers and + - * / ( )."

TOOL_FUNCTIONS = {
    "get_item_price": get_item_price,
    "get_venue_charge": get_venue_charge,
    "calculate_event_cost": calculate_event_cost
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_item_price",
            "description": "Get the price of one campus event item.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "Event item name"
                    },
                    "category": {
                        "type": "string",
                        "enum": [
                            "equipment",
                            "furniture",
                            "printing",
                            "stationery"
                        ],
                        "description": "Item category"
                    }
                },
                "required": ["item"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_venue_charge",
            "description": "Get the venue charge for a campus event.",
            "parameters": {
                "type": "object",
                "properties": {
                    "venue_type": {
                        "type": "string",
                        "enum": [
                            "classroom",
                            "seminar_hall",
                            "auditorium"
                        ],
                        "description": "Campus venue type"
                    }
                },
                "required": ["venue_type"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_event_cost",
            "description": "Calculate a numeric event budget expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Arithmetic expression using numbers and operators"
                    }
                },
                "required": ["expression"],
                "additionalProperties": False
            }
        }
    }
]

SCHEMAS = {
    tool["function"]["name"]: tool["function"]["parameters"]
    for tool in TOOLS
}
