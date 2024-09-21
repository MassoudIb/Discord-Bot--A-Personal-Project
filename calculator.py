# Author : Massoud Ibrahim
# Date 2024-06-04
# calculator.py file has the function required for /calc command.

import math

allowed_operations = {
    'math': math,
    '__builtins__': {},   # disallow all built-ins
    'abs': abs,
    'round': round,
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'pi': math.pi,
    'e': math.e,
    'exp': math.exp,
    'log': math.log,
    'log10': math.log10,
    'factorial': math.factorial,
    'pow': pow
}

def eval_expression(expression):
    try:
        expression = expression.replace('^', '**')
        code = compile(expression, "<string>", "eval")
        for operation in code.co_names:
            if operation not in allowed_operations:
                raise NameError(f"Use of {operation} is not allowed")
        return eval(code, {"__builtins__": None}, allowed_operations)
    except Exception as e:
        return str(e)
