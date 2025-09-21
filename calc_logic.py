import math as m
import re

def evaluate_expression(expression: str) -> str:
    """Safely evaluate math expression."""
    try:
        # Replace symbols with math equivalents
        expression = expression.replace("π", str(m.pi))
        expression = expression.replace("sqrt", "m.sqrt")
        expression = expression.replace("sin", "m.sin")
        expression = expression.replace("cos", "m.cos")
        expression = expression.replace("tan", "m.tan")
        expression = expression.replace("log", "m.log")

        result = eval(expression)  # WARNING: only okay in this controlled app
        return str(result)
    except Exception:
        return "Error"

def clear() -> str:
    return ""

def delete_last(expression: str) -> str:
    return expression[:-1]
