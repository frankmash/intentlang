Here is a cleaned-up and properly structured version of your **README.md** content:

```markdown
# IntentLang

**IntentLang** is a lightweight, rule-based programming language designed for expressing  
**decision logic, policies, and state mutations** outside of application code.

It is built to make business rules, permissions, feature flags, and policies  
**human-readable, auditable, and safe**.



## Why IntentLang?

Most applications hard-code decision logic inside JavaScript, Python, etc.  

**IntentLang** cleanly separates **what the system decides** from **how the system runs**.

Benefits:

- Easier to reason about
- Safer to change
- Easier to audit
- Friendlier to non-developers (business analysts, compliance, product, legal, etc.)

---

## Example

```intent
rule "adult verification" {
  when user.age >= 18
  then
    user.is_verified = true
}
```

```intent
rule "premium discount eligibility" {
  when
    user.country == "KE" and
    user.subscription_plan == "basic" and
    now() < user.trial_ends_at
  then
    order.discount_percentage += 15
}
```


## Quick Start

### 1. Install (from source – for now)

```bash
git clone <your-repo-url>
cd intentlang
pip install -e .
```

(PyPI package coming soon.)

### 2. Write a rule file

`verify.intent`:

```intent
rule "adult verification" {
  when user.age >= 18
  then
    user.is_verified = true
}
```

### 3. Run from Python

```python
from lark import Lark

from intentlang.runtime import run
from intentlang.transform import ToAST
from intentlang.grammar import GRAMMAR

rules_text = open("verify.intent").read()

parser = Lark(
    GRAMMAR,
    start="start",
    parser="lalr",
    transformer=ToAST()
)

rules = parser.parse(rules_text)

context = {
    "user": {"age": 21}
}

result = run(rules, context, mode="apply")

print(result)
```

**Example output:**

```json
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
```


## Core Concepts

### Rules

Each rule has:

- A name (quoted string)
- A `when` condition
- One or more `then` mutations

### Conditions

Pure expressions — no side effects, fully deterministic.

**Supported:**

- Comparisons: `== != > >= < <=`
- Logical: `and or`
- Grouping: `( … )`

### Mutations

Describe *intended* state changes (not executed during evaluation).

**Supported operations:**

- `path = value`
- `path += number`
- `path -= number`

Properties: explicit, conflict-checked, only applied by the runtime.


## Execution Modes

| Mode   | Evaluates rules | Returns effects plan | Actually mutates context |
|--------|------------------|-----------------------|---------------------------|
| `dry`  | Yes              | No                    | No                        |
| `plan` | Yes              | Yes                   | No                        |
| `apply`| Yes              | Yes                   | Yes                       |

Safe by default.



## Conflict Detection

If multiple rules try to modify the **same path** in one evaluation,  
IntentLang raises a conflict error instead of overwriting silently.

Guarantees: **determinism · predictability · safety**


## Use Cases

Ideal for:

- Feature flags & progressive rollouts
- Permissions / RBAC / ABAC
- Business rules & approval workflows
- Pricing, discounts, promotions
- Game mechanics & progression systems
- Regulatory / compliance policies
- AI output filters & safety guardrails

Not meant to replace general-purpose languages.



## Architecture Overview

```
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
```



## Status

- **Version**: v0.1 (early development)
- Language syntax mostly stable
- Suitable for experiments and non-critical production use
- API and developer tooling still evolving



## License

[MIT License](LICENSE) — free for personal and commercial use.


## Philosophy

IntentLang is **intentionally small**.

Goals:

- Understandable
- Composable
- Safe
- Boring (in the best possible way)

**Complexity belongs in applications.**  
**Decisions belong in rules.**
```