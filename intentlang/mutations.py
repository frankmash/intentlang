from .node import Mutation


class MutationError(Exception):
    pass


def build_effect(mutation: Mutation):
    """
    Convert a Mutation AST node into a declarative effect.
    """

    if mutation.operator == "=":
        return {
            "op": "set",
            "path": mutation.path,
            "value": mutation.value
        }

    if mutation.operator == "+=":
        return {
            "op": "increment",
            "path": mutation.path,
            "value": mutation.value
        }

    if mutation.operator == "-=":
        return {
            "op": "decrement",
            "path": mutation.path,
            "value": mutation.value
        }

    raise MutationError(f"Unknown mutation operator '{mutation.operator}'")


def collect_effects(mutations):
    """
    Convert a list of Mutation nodes into a list of effects.
    """
    effects = []

    for mutation in mutations:
        effects.append(build_effect(mutation))

    return effects
