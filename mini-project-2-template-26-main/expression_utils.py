"""Shared helpers for both Questions pages: wraps EvaluateExpression from
library.py (Exercise 1) so no user input can ever crash a page."""

import math

from library import EvaluateExpression


# rewrite unary minus with algebra (-x = 0-x) so the two-stack evaluator,
# which only knows binary operators, can handle negative numbers:
# "-2+3" -> "(0-2)+3",  "2*-3" -> "2*(0-3)",  "-(2+3)" -> "(0-(2+3))"
def rewrite_unary_minus(expression):
    out = ""
    i = 0
    while i < len(expression):
        ch = expression[i]
        prev = out.rstrip()[-1:]
        # a minus is unary when it starts the expression or follows an operator or "("
        if ch == "-" and (prev == "" or prev in "+-*/("):
            k = i + 1
            while k < len(expression) and expression[k] == " ":
                k += 1
            # minus before a number: wrap the number as (0-number)
            if k < len(expression) and (expression[k].isdigit() or expression[k] == "."):
                m = k
                while m < len(expression) and (expression[m].isdigit() or expression[m] == "."):
                    m += 1
                out += "(0-" + expression[k:m] + ")"
                i = m
                continue
            # minus before a bracket: wrap the whole group as (0-(...))
            if k < len(expression) and expression[k] == "(":
                depth, m = 0, k
                while m < len(expression):
                    if expression[m] == "(":
                        depth += 1
                    elif expression[m] == ")":
                        depth -= 1
                        if depth == 0:
                            break
                    m += 1
                if m < len(expression):
                    out += "(0-(" + rewrite_unary_minus(expression[k + 1:m]) + "))"
                    i = m + 1
                    continue
        out += ch
        i += 1
    return out


# evaluate an expression and return (answer, error): exactly one of them is None
def safe_evaluate(expression):
    if not expression.strip():
        return None, "The expression is empty."
    if EvaluateExpression(expression).expression == "":
        return None, "Invalid characters: only digits, + - * / ( ) . and spaces are allowed."

    evaluator = EvaluateExpression(rewrite_unary_minus(expression))

    # a valid infix expression has exactly one more number than operators,
    # so inputs like "2 3" are rejected instead of silently returning 3
    tokens = evaluator.insert_space().split()
    operands = [t for t in tokens if t not in "+-*/()"]
    operators = [t for t in tokens if t in "+-*/"]
    if len(operands) != len(operators) + 1:
        return None, "Incomplete expression: every operator needs a number on both sides."

    # each failure mode gets its own specific message instead of a crash
    try:
        answer = evaluator.evaluate()
    except IndexError:
        return None, "Malformed expression: check that operators and brackets are complete."
    except ZeroDivisionError:
        return None, "Division by zero is undefined."
    except ValueError:
        return None, "Malformed number in the expression."
    if answer is None or not math.isfinite(answer):
        return None, "The result is too large to store as an answer."
    return answer, None
