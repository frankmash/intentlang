from .evaluator import evaluate
from .mutations import collect_effects, MutationError
from .explain import RuleExplanation, ConditionExplanation
from .evaluator import evaluate, explain


# ============================
# ERRORS
# ============================

class RuntimeError(Exception):
    pass


class ConflictError(Exception):
    pass


# ============================
# EFFECT APPLICATION
# ============================

def apply_effect(effect, context):
    """
    Apply a single effect to the context (in-place).
    """
    path_parts = effect["path"].split(".")
    target = context

    # Walk down to parent object
    for key in path_parts[:-1]:
        if key not in target or not isinstance(target[key], dict):
            target[key] = {}
        target = target[key]

    field = path_parts[-1]

    if effect["op"] == "set":
        target[field] = effect["value"]

    elif effect["op"] == "increment":
        target[field] = target.get(field, 0) + effect["value"]

    elif effect["op"] == "decrement":
        target[field] = target.get(field, 0) - effect["value"]

    else:
        raise RuntimeError(f"Unknown effect operation '{effect['op']}'")


# ============================
# CONFLICT DETECTION
# ============================

def detect_conflicts(effects):
    """
    Detect multiple mutations to the same path in a single run.
    """
    seen = {}

    for effect in effects:
        path = effect["path"]
        rule = effect.get("rule", "<unknown>")

        if path in seen:
            raise ConflictError(
                f"Conflict detected on '{path}' "
                f"(rules '{seen[path]}' and '{rule}')"
            )

        seen[path] = rule


# ============================
# RUNTIME EXECUTION
# ============================

def run(rules, context, mode="plan"):
    """
    Execute rules against a context.

    Modes:
    - dry   → evaluate rules only (no effects)
    - plan  → return effects (no mutation)
    - apply → apply effects to context
    """

    if mode not in ("dry", "plan", "apply"):
        raise RuntimeError(f"Invalid mode '{mode}'")

    results = {
    "matched_rules": [],
    "effects": [],
    "context": context,
    "explanations": []
}


    # Evaluate rules & collect effects
    from .evaluator import evaluate, explain
from .mutations import collect_effects, MutationError
from .explain import RuleExplanation, ConditionExplanation


# ============================
# ERRORS
# ============================

class RuntimeError(Exception):
    pass


class ConflictError(Exception):
    pass


# ============================
# EFFECT APPLICATION
# ============================

def apply_effect(effect, context):
    """
    Apply a single effect to the context (in-place).
    """
    path_parts = effect["path"].split(".")
    target = context

    # Walk down to parent object
    for key in path_parts[:-1]:
        if key not in target or not isinstance(target[key], dict):
            target[key] = {}
        target = target[key]

    field = path_parts[-1]

    if effect["op"] == "set":
        target[field] = effect["value"]

    elif effect["op"] == "increment":
        target[field] = target.get(field, 0) + effect["value"]

    elif effect["op"] == "decrement":
        target[field] = target.get(field, 0) - effect["value"]

    else:
        raise RuntimeError(f"Unknown effect operation '{effect['op']}'")


# ============================
# CONFLICT DETECTION
# ============================

def detect_conflicts(effects):
    """
    Detect multiple mutations to the same path in a single run.
    """
    seen = {}

    for effect in effects:
        path = effect["path"]
        rule = effect.get("rule", "<unknown>")

        if path in seen:
            raise ConflictError(
                f"Conflict detected on '{path}' "
                f"(rules '{seen[path]}' and '{rule}')"
            )

        seen[path] = rule


# ============================
# RUNTIME EXECUTION
# ============================

def run(rules, context, mode="plan"):
    """
    Execute rules against a context.

    Modes:
    - dry   → evaluate rules only (no effects)
    - plan  → return effects (no mutation)
    - apply → apply effects to context
    """

    if mode not in ("dry", "plan", "apply"):
        raise RuntimeError(f"Invalid mode '{mode}'")

    results = {
        "matched_rules": [],
        "effects": [],
        "context": context,
        "explanations": []
    }

    # Evaluate rules & collect explanations
    for rule in rules:
        rule_expl = RuleExplanation(
            rule_name=rule.name,
            matched=False
        )

        result, details = explain(rule.condition, context)

        rule_expl.conditions.append(
            ConditionExplanation(
                expression=str(rule.condition),
                result=result,
                details=details
            )
        )

        if result:
            rule_expl.matched = True
            results["matched_rules"].append(rule.name)

            try:
                effects = collect_effects(rule.mutations)
            except MutationError as e:
                raise RuntimeError(str(e))

            for effect in effects:
                effect["rule"] = rule.name
                results["effects"].append(effect)
                rule_expl.mutations.append(
                    f"{effect['path']} {effect['op']} {effect['value']}"
                )

        # ALWAYS append explanation
        results["explanations"].append(rule_expl)

    # Detect conflicts before applying
    if mode in ("plan", "apply"):
        detect_conflicts(results["effects"])

    # Apply effects if requested
    if mode == "apply":
        for effect in results["effects"]:
            apply_effect(effect, context)

    # Dry mode returns no effects
    if mode == "dry":
        results.pop("effects")

    return results


    # Detect conflicts before applying
    if mode in ("plan", "apply"):
        detect_conflicts(results["effects"])

    #Apply effects if requested
    if mode == "apply":
        for effect in results["effects"]:
            apply_effect(effect, context)

    #Dry mode returns no effects
    if mode == "dry":
        results.pop("effects")

    return results
