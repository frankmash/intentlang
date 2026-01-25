# IntentLang

IntentLang is a lightweight, **rule-based** programming language designed for expressing  
**decision logic, policies, and state mutations** outside of application code.

It is built to make business rules, permissions, feature flags, and policies  
**human-readable, auditable, and safe**.

---

## Why IntentLang?

Most applications hard-code decision logic inside JavaScript, Python, etc.

**IntentLang** separates **what the system decides** from **how the system runs**.

This makes systems:

- Easier to reason about
- Safer to change
- Easier to audit
- Friendlier to non-developers (business analysts, compliance, product, etc.)

---

## Example

```intent
rule "adult verification" {
  when user.age >= 18
  then
    user.is_verified = true
}
intent
Copy code
rule "premium discount eligibility" {
  when
    user.country == "KE" and
    user.subscription_plan == "basic" and
    now() < user.trial_ends_at
  then
    order.discount_percentage += 15
}
Quick Start
1. Install
bash
Copy code
pip install -e .
For now, install from source. PyPI support is planned.

2. Write a rule
Create a file verify.intent:

intent
Copy code
rule "adult verification" {
  when user.age >= 18
  then
    user.is_verified = true
}
3. Run from Python
python
Copy code
from lark import Lark
from intentlang.runtime import run
from intentlang.transform import ToAST
from intentlang.grammar import GRAMMAR

rules_text = open("verify.intent").read()

parser = Lark(GRAMMAR, start="start", parser="lalr", transformer=ToAST())
rules = parser.parse(rules_text)

context = {
    "user": {"age": 21}
}

result = run(rules, context, mode="apply")
print(result)
Output
json
Copy code
{
  "matched_rules": ["adult verification"],
  "effects": [
    {
      "op": "set",
      "path": "user.is_verified",
      "value": true,
      "rule": "adult verification"
    }
  ],
  "context": {
    "user": {
      "age": 21,
      "is_verified": true
    }
  }
}
Core Concepts
Rules
A rule consists of:

A name (quoted string)

A condition (when clause)

One or more mutations (then clause)

Conditions
Conditions are pure expressions:

No side effects

Deterministic

Evaluated against the input context

Supported operators:

Comparisons: ==, !=, >, >=, <, <=

Logical: and, or

Parentheses for grouping

Mutations
Mutations describe intended state changes (not immediate execution).

Supported operations:

Assignment: =

Increment: +=

Decrement: -=

Mutations are:

Explicit

Conflict-checked

Only applied by the runtime (never during evaluation)

Execution Modes
IntentLang supports three safe-by-default execution modes:

Mode	Evaluates rules	Returns planned effects	Applies changes
dry	Yes	No	No
plan	Yes	Yes	No
apply	Yes	Yes	Yes

Conflict Detection
If two rules try to mutate the same path in a single run, IntentLang raises a
conflict error instead of silently overwriting.

This guarantees:

Determinism

Predictability

Safety

Use Cases
IntentLang is well-suited for:

Feature flags & rollouts

Permissions & role-based access control

Business rules & workflows

Pricing & discount logic

Game mechanics & progression rules

Policy & compliance engines

AI output guardrails & safety filters

It is not intended to replace general-purpose programming languages.

Architecture Overview
text
Copy code
Text (.intent files)
      ↓
Parser (Lark)
      ↓
AST + semantic model
      ↓
Evaluator → condition results (true/false)
      ↓
Mutation planner → ordered, conflict-checked plan
      ↓
Runtime (dry / plan / apply)
Status
Version: v0.1 (early development)

Language syntax is mostly stable

Suitable for experimentation and non-critical real-world use

API and tooling are still evolving

License
MIT License — free for personal and commercial use.

Philosophy
IntentLang is intentionally small.

It aims to be:

Understandable

Composable

Safe

Boring (in the best possible way)

Complexity belongs in applications.
Decisions belong in rules.