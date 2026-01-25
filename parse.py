from lark import Lark
from transform import ToAST
from runtime import run

with open("grammar.lark") as f:
    grammar = f.read()

parser = Lark(
    grammar,
    start="start",
    parser="lalr",
    transformer=ToAST()
)

program = """
rule "adult verification" {
  when user.age >= 18
  then
    user.is_verified = true
}
"""

rules = parser.parse(program)

context = {
    "user": {"age": 21}
}

result = run(rules, context, mode="apply")

print(result)
print("Final context:", context)
