from datetime import datetime, timezone
from .node import Comparison, And, Or, FunctionCall
from collections.abc import Iterable
from .node import Comparison, And, Or, Not, FunctionCall



class EvaluationError(Exception):
    pass


def get_value_from_path(context, path):
    parts = path.split(".")
    current = context

    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            raise EvaluationError(f"Path '{path}' not found in context")

    return current


def path_exists(context, path):
    parts = path.split(".")
    current = context

    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False

    return True


def parse_datetime(value):
    """
    Accept datetime or ISO-8601 string.
    """
    if isinstance(value, datetime):
        return value

    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            raise EvaluationError(f"Invalid datetime string: {value}")

    return value


def eval_comparison(expr: Comparison, context):
    left = evaluate(expr.left, context)
    right = evaluate(expr.right, context)

    op = expr.operator

    if op == "==":
        return left == right
    if op == "!=":
        return left != right
    if op == ">":
        return left > right
    if op == ">=":
        return left >= right
    if op == "<":
        return left < right
    if op == "<=":
        return left <= right

    raise EvaluationError(f"Unknown operator '{op}'")



def eval_function_call(expr: FunctionCall, context):
    name = expr.name
    args = expr.args

    # -------- exists(path) --------
    if name == "exists":
        if len(args) != 1:
            raise EvaluationError("exists() expects exactly one argument")

        arg = args[0]
        if not isinstance(arg, str):
            raise EvaluationError("exists() argument must be a path")

        return path_exists(context, arg)

    # -------- now() --------
    if name == "now":
        if args:
            raise EvaluationError("now() takes no arguments")

        return datetime.now(timezone.utc)

    # -------- len(value) --------
    if name == "len":
        if len(args) != 1:
            raise EvaluationError("len() expects exactly one argument")

        value = evaluate(args[0], context)

        if not isinstance(value, (str, list, dict, tuple)):
            raise EvaluationError("len() argument must be a collection or string")

        return len(value)

    # -------- contains(collection, value) --------
    if name == "contains":
        if len(args) != 2:
            raise EvaluationError("contains() expects exactly two arguments")

        collection = evaluate(args[0], context)
        value = evaluate(args[1], context)

        if not isinstance(collection, Iterable):
            raise EvaluationError("contains() first argument must be a collection")

        return value in collection

    raise EvaluationError(f"Unknown function '{name}'")



def evaluate(expr, context):
    # Literal values
    if isinstance(expr, (int, float, bool)):
        return expr

    # Path reference
    if isinstance(expr, str):
        return get_value_from_path(context, expr)

    if isinstance(expr, Comparison):
        return eval_comparison(expr, context)

    if isinstance(expr, And):
        return evaluate(expr.left, context) and evaluate(expr.right, context)

    if isinstance(expr, Or):
        return evaluate(expr.left, context) or evaluate(expr.right, context)

    if isinstance(expr, FunctionCall):
        return eval_function_call(expr, context)
    
    if isinstance(expr, Not):
        return not evaluate(expr.expr, context)

    raise EvaluationError(f"Unknown expression type: {type(expr)}")
    
    



