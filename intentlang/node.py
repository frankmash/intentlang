from dataclasses import dataclass
from typing import List, Any


# ========= EXPRESSIONS =========

@dataclass
class Expr:
    pass


@dataclass
class Comparison(Expr):
    path: str
    operator: str
    value: Any


@dataclass
class And(Expr):
    left: Expr
    right: Expr


@dataclass
class Or(Expr):
    left: Expr
    right: Expr


# ========= MUTATIONS =========

@dataclass
class Mutation:
    path: str
    operator: str
    value: Any


# ========= RULE =========

@dataclass
class Rule:
    name: str
    condition: Expr
    mutations: List[Mutation]
