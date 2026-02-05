from lark import Lark, exceptions

from intentlang.grammar import GRAMMAR
from intentlang.transform import ToAST


def parse_ok(source: str):
    parser = Lark(
        GRAMMAR,
        start="start",
        parser="lalr",
        transformer=ToAST(),
    )
    return parser.parse(source)


def parse_fail(source: str):
    try:
        parse_ok(source)
    except exceptions.LarkError:
        return True
    return False


# ----------------------------
# VALID SYNTAX TESTS
# ----------------------------

def test_simple_comparison():
    parse_ok("""
    rule "age check" {
      when user.age >= 18
      then
        user.allowed = true
    }
    """)


def test_exists_function():
    parse_ok("""
    rule "trial check" {
      when exists(user.trial_ends_at)
      then
        user.is_on_trial = true
    }
    """)


def test_now_comparison():
    parse_ok("""
    rule "time window" {
      when now() < user.trial_ends_at
      then
        user.active = true
    }
    """)


def test_len_function():
    parse_ok("""
    rule "multi role" {
      when len(user.roles) > 1
      then
        user.is_power = true
    }
    """)


def test_contains_function():
    parse_ok("""
    rule "admin access" {
      when contains(user.roles, "admin")
      then
        user.is_admin = true
    }
    """)


def test_complex_expression():
    parse_ok("""
    rule "complex" {
      when exists(user.roles)
       and len(user.roles) > 0
       and contains(user.roles, "admin")
       or user.is_superuser == true
      then
        user.can_access = true
    }
    """)


# ----------------------------
# INVALID SYNTAX TESTS
# ----------------------------

def test_missing_when():
    assert parse_fail("""
    rule "invalid" {
      user.age >= 18
      then
        user.allowed = true
    }
    """)


def test_invalid_function_call():
    assert parse_fail("""
    rule "bad func" {
      when len()
      then
        user.allowed = true
    }
    """)


def test_invalid_operator():
    assert parse_fail("""
    rule "bad op" {
      when user.age === 18
      then
        user.allowed = true
    }
    """)
