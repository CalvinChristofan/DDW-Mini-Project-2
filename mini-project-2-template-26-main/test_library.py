from library import EvaluateExpression, Stack
import pytest

def test_init_property():
    expr1 = EvaluateExpression()
    assert expr1.expression == ""
    expr2 = EvaluateExpression("1 + 2")
    assert expr2.expression == "1 + 2"
    expr2.expression = "3 * 4"
    assert expr2.expression == "3 * 4"
    expr2.expression = "3 & 4"
    assert expr2.expression == ""

def test_insert_space():
    expr1 = EvaluateExpression("(1+2)")
    assert expr1.insert_space() == " ( 1 + 2 ) "
    expr1.expression = "((1+2)*3/(4-5))"
    assert expr1.insert_space() == " (  ( 1 + 2 )  * 3 /  ( 4 - 5 )  ) "

def test_process_operator():
    expr1 = EvaluateExpression()
    operand_stack = Stack()
    operator_stack = Stack()
    operand_stack.push(3)
    operand_stack.push(4)
    operator_stack.push("+")
    expr1.process_operator(operand_stack, operator_stack)
    assert operand_stack.peek() == 7
    operand_stack.push(5)
    operator_stack.push("*")
    expr1.process_operator(operand_stack, operator_stack)
    assert operand_stack.peek() == 35
    operand_stack.push(30)
    operator_stack.push("-")
    expr1.process_operator(operand_stack, operator_stack)
    assert operand_stack.peek() == 5
    operand_stack.push(2)
    operator_stack.push("/")
    expr1.process_operator(operand_stack, operator_stack)
    assert operand_stack.peek() == 2.5

def test_evaluate():
    assert EvaluateExpression().evaluate() is None
    expr1 = EvaluateExpression("(1+2)*3")
    assert expr1.evaluate() == 9
    expr1.expression = "(1 + 2) * 4 - 3"
    assert expr1.evaluate() == 9
    expr2 = EvaluateExpression("(1+2 *4-  3)* (7/5 * 6)")
    assert abs(expr2.evaluate() - 50.4) < 0.001
    expr3 = EvaluateExpression("(1.2+2 *4-  3)* (7/5 * 6)")
    assert abs(expr3.evaluate() - 52.08) < 0.001
