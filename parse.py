from lark import Lark
from intentlang.transform import ToAST
from intentlang.runtime import run
from intentlang.grammar import GRAMMAR

parser = Lark(
    GRAMMAR,
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
