TYPES = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict
}

def validate_arguments(arguments, schema):
    if not isinstance(arguments, dict):
        return "Arguments must be a JSON object."

    properties = schema.get("properties", {})

    for name in schema.get("required", []):
        if name not in arguments:
            return f"Missing required argument '{name}'. Expected: {', '.join(properties)}."

    if schema.get("additionalProperties") is False:
        extra = [key for key in arguments if key not in properties]

        if extra:
            return f"Unexpected argument(s): {', '.join(extra)}. Allowed: {', '.join(properties)}."

    for name, value in arguments.items():
        rule = properties.get(name, {})
        expected = TYPES.get(rule.get("type"))

        if expected and not isinstance(value, expected):
            return f"Argument '{name}' must be a {rule['type']}, but got {type(value).__name__}: {value!r}."

        if "enum" in rule and value not in rule["enum"]:
            return f"Argument '{name}' must be one of {rule['enum']}, got {value!r}."

    return None

if __name__ == "__main__":
    from tools_v2 import SCHEMAS

    schema = SCHEMAS["get_venue_charge"]

    cases = [
        {"venue_type": "auditorium"},
        {"venue_type": "seminar_hall"},
        {},
        {"venue_type": 101},
        {"venue_type": "playground"},
        {"venue_type": "auditorium", "year": 2026}
    ]

    for case in cases:
        result = validate_arguments(case, schema)
        print(f"{str(case):<60} -> {result or 'OK'}")
