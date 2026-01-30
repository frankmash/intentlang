from datetime import datetime, timezone
from .node import Comparison, And, Or, FunctionCall


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
    left = get_value_from_path(context, expr.path)
    right = expr.value
    op = expr.operator

    # Normalize datetimes if needed
    left = parse_datetime(left)
    right = parse_datetime(right)

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

    if name == "exists":
        if len(args) != 1:
            raise EvaluationError("exists() expects exactly one argument")

        arg = args[0]
        if not isinstance(arg, str):
            raise EvaluationError("exists() argument must be a path")

        return path_exists(context, arg)

    if name == "now":
        if args:
            raise EvaluationError("now() takes no arguments")

        return datetime.now(timezone.utc)

    raise EvaluationError(f"Unknown function '{name}'")


def evaluate(expr, context):
    if isinstance(expr, Comparison):
        return eval_comparison(expr, context)

    if isinstance(expr, And):
        return evaluate(expr.left, context) and evaluate(expr.right, context)

    if isinstance(expr, Or):
        return evaluate(expr.left, context) or evaluate(expr.right, context)

    if isinstance(expr, FunctionCall):
        return eval_function_call(expr, context)

    raise EvaluationError(f"Unknown expression type: {type(expr)}")
