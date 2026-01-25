from lark import Transformer
from .node import Rule, Comparison, And, Or, Mutation


class ToAST(Transformer):

    # ---------- ROOT ----------
    def start(self, items):
        return items

    # ---------- SYNTAX UNWRAPPING ----------
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
        path, op, value = items
        return Comparison(path, str(op), value)

    def and_expr(self, items):
        return And(items[0], items[1])

    def or_expr(self, items):
        return Or(items[0], items[1])

    # ---------- MUTATIONS ----------
    def mutation(self, items):
        path, op, value = items
        return Mutation(path, str(op), value)

    # ---------- RULE ----------
    def rule(self, items):
        name, condition, mutations = items
        return Rule(name, condition, mutations)
