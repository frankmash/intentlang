from lark import Lark
from intentlang.grammar import GRAMMAR
from intentlang.transform import ToAST
from intentlang.runtime import run

# Load rules
rules_text = open("examples/verify.intent").read()

parser = Lark(
    GRAMMAR,
    start="start",
    parser="lalr",
    transformer=ToAST()
)

rules = parser.parse(rules_text)

# Context to test
context = {
    "user": {
        "age": 21,
        "roles": ["admin"]
    }
}

result = run(rules, context, mode="apply")
print(result)
