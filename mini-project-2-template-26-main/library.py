class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop()

    def peek(self):
        return self._items[-1]

    @property
    def is_empty(self):
        return len(self._items) == 0

    @property
    def size(self):
        return len(self._items)


class EvaluateExpression:
    valid_char = "0123456789+-*/(). "

    def __init__(self, string=""):
        self.expression = string

    @property
    def expression(self):
        return self._expression

    @expression.setter
    def expression(self, new_expr):
        for char in new_expr:
            if char not in EvaluateExpression.valid_char:
                self._expression = ""
                return
        self._expression = new_expr

    def insert_space(self):
        spaced = ""
        for char in self.expression:
            if char in "+-*/()":
                spaced += " " + char + " "
            else:
                spaced += char
        return spaced

    def process_operator(self, operand_stack, operator_stack):
        operator = operator_stack.pop()
        right = operand_stack.pop()
        left = operand_stack.pop()
        if operator == "+":
            operand_stack.push(left + right)
        elif operator == "-":
            operand_stack.push(left - right)
        elif operator == "*":
            operand_stack.push(left * right)
        elif operator == "/":
            operand_stack.push(left / right)

    def evaluate(self):
        if self.expression == "":
            return None
        operand_stack = Stack()
        operator_stack = Stack()
        expression = self.insert_space()
        tokens = expression.split()
        for token in tokens:
            if token == "+" or token == "-":
                while (not operator_stack.is_empty and
                       operator_stack.peek() in "+-*/"):
                    self.process_operator(operand_stack, operator_stack)
                operator_stack.push(token)
            elif token == "*" or token == "/":
                while (not operator_stack.is_empty and
                       operator_stack.peek() in "*/"):
                    self.process_operator(operand_stack, operator_stack)
                operator_stack.push(token)
            elif token == "(":
                operator_stack.push(token)
            elif token == ")":
                while operator_stack.peek() != "(":
                    self.process_operator(operand_stack, operator_stack)
                operator_stack.pop()
            else:
                operand_stack.push(float(token))
        while not operator_stack.is_empty:
            self.process_operator(operand_stack, operator_stack)
        return operand_stack.pop()