from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class ConditionExplanation:
    expression: str
    result: bool
    details: str


@dataclass
class RuleExplanation:
    rule_name: str
    matched: bool
    conditions: List[ConditionExplanation] = field(default_factory=list)
    mutations: List[str] = field(default_factory=list)
