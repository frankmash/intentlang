from lark import Transformer
from .node import Rule, Comparison, And, Or, Mutation, FunctionCall


class ToAST(Transformer):

    # ---------- ROOT ----------
    def start(self, items):
        return items

    # ---------- STRUCTURE ----------
    def when(self, items):
        return items[0]

    def then(self, items):
        return items

    # ---------- PRIMITIVES ----------
    def STRING(self, s):
        return s[1:-1]

    def NUMBER(self, n):
        return int(n)

    def BOOLEAN(self, b):
        return b == "true"

    def path(self, items):
        return ".".join(items)

    def value(self, items):
        return items[0]

    # ---------- EXPRESSIONS ----------
    def comparison(self, items):
        left, op, right = items
        return Comparison(left, str(op), right)

    def and_expr(self, items):
        return And(items[0], items[1])

    def or_expr(self, items):
        return Or(items[0], items[1])

    def function_call(self, items):
        name = str(items[0])
        args = items[1:] if len(items) > 1 else []
        return FunctionCall(name, args)

    # ---------- MUTATIONS ----------
    def mutation(self, items):
        path, op, value = items
        return Mutation(path, str(op), value)

    # ---------- RULE ----------
    def rule(self, items):
        name = items[0]
        condition = items[1]
        mutations = items[2]
        return Rule(name, condition, mutations)
