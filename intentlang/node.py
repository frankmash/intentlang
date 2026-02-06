from dataclasses import dataclass
from typing import List, Any
from dataclasses import dataclass


# ========= EXPRESSIONS =========

@dataclass
class Expr:
    pass


@dataclass
class Comparison(Expr):
    left: Expr
    operator: str
    right: Expr


@dataclass
class And(Expr):
    left: Expr
    right: Expr


@dataclass
class Or(Expr):
    left: Expr
    right: Expr


@dataclass
class FunctionCall(Expr):
    name: str
    args: List[Expr]


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


@dataclass
class Not(Expr):
    expr: Expr
