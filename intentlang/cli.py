import argparse
import json
import sys
from lark import Lark

from .grammar import GRAMMAR
from .transform import ToAST
from .runtime import run


def load_rules(path):
    with open(path, "r") as f:
        text = f.read()

    parser = Lark(
        GRAMMAR,
        start="start",
        parser="lalr",
        transformer=ToAST()
    )

    return parser.parse(text)


def load_context(path):
    with open(path, "r") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        prog="intent",
        description="IntentLang CLI"
    )

    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run rules against context")
    run_parser.add_argument("rules", help="Path to .intent file")
    run_parser.add_argument("context", help="Path to JSON context file")
    run_parser.add_argument(
        "--mode",
        choices=["dry", "plan", "apply"],
        default="plan",
        help="Execution mode"
    )

    args = parser.parse_args()

    if args.command == "run":
        rules = load_rules(args.rules)
        context = load_context(args.context)

        result = run(rules, context, mode=args.mode)

        print(json.dumps(result, indent=2, default=str))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
