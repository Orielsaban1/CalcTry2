import re
import math
from abc import ABC, abstractmethod
from typing import List

class Operator(ABC):
    def __init__(self, symbol: str, power: int, arity: int, side_oper: bool = False):
        self.symbol = symbol
        self.power = power
        self.arity = arity
        self.side_oper = side_oper

    @abstractmethod
    def execute(self, num1,num2):
        pass
    @abstractmethod
    def execute(self, num1):
        pass
class Favtorial(Operator):
    def __init__(self):
        super().__init__("!", 7, 1)

    def execute(self, num1: float):
        if num1 < 0 or not isinstance(num1, int):
            raise TypeError("Factorial requires a non-negative integer")
        return float(math.factorial(int(num1)))

class Negative(Operator):
    def __init__(self):
        super().__init__("~", 6, 1, True)

    def execute(self, num1: float):
        return float((-1) * num1)

class Max(Operator):
    def __init__(self):
        super().__init__("@", 5, 2)

    def execute(self, num1: float, num2: float):
        return float(max(num1, num2))

class Min(Operator):
    def __init__(self):
        super().__init__("&", 5, 2)

    def execute(self, num1: float, num2: float):
        return float(min(num1, num2))

class Averge(Operator):
    def __init__(self):
        super().__init__("$", 5, 2)

    def execute(self, num1: float, num2: float):
        return float((num1 + num2) / 2)

class Modulo(Operator):
    def __init__(self):
        super().__init__("%", 4, 2)

    def execute(self, num1: float, num2: float):
        return float(num1 % num2)

class Power(Operator):
    def __init__(self):
        super().__init__("^", 3, 2)

    def execute(self, num1: float, num2: float):
        return float(num1 ** num2)

class Multiply(Operator):
    def __init__(self):
        super().__init__("*", 2, 2)

    def execute(self, num1: float, num2: float):
        return float(num1) * float(num2)

class Divide(Operator):
    def __init__(self):
        super().__init__("/", 2, 2)

    def execute(self, num1: float, num2: float):
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        return float(num1) / float(num2)

class Minus(Operator):
    def __init__(self):
        super().__init__("-", 1, 2)

    def execute(self, num1: float, num2: float):
        return float(num1) - float(num2)

class Plus(Operator):
    def __init__(self):
        super().__init__("+", 1, 2)

    def execute(self, num1: float, num2: float):
        return float(num1) + float(num2)

class MathOperation:
    def __init__(self):
        self.plus = Plus()
        self.minus = Minus()
        self.divide = Divide()
        self.multiply = Multiply()
        self.power = Power()
        self.modulo = Modulo()
        self.minimum = Min()
        self.maximum = Max()
        self.averge = Averge()
        self.negative = Negative()
        self.factorial = Favtorial()
        self.operators = {
            '!': self.factorial, '~': self.negative, '@': self.maximum, '&': self.minimum, '$': self.averge,
            '%': self.modulo, '^': self.power, '*': self.multiply, '/': self.divide, '+': self.plus, '-': self.minus
        }
        if len(self.operators) != len(set(self.operators.keys())):
            raise ValueError("Duplicate keys found in operators dictionary!")


class Node(ABC):
    @abstractmethod
    def execute(self) -> float:
        pass

class NumberNode(Node):
    def __init__(self, value: float):
        self.value = value

    def execute(self) -> float:
        return self.value

class UnaryOpNode(Node):
    def __init__(self, op: Operator, child: Node):
        self.op = op
        self.child = child

    def execute(self) -> float:
        return self.op.execute(self.child.execute())

class BinaryOpNode(Node):
    def __init__(self, op: Operator, left: Node, right: Node):
        self.op = op
        self.left = left
        self.right = right

    def execute(self) -> float:
        return self.op.execute(self.left.execute(), self.right.execute())

class Parser:
    def __init__(self, tokens: List[str], operators: dict):
        self.tokens = tokens
        self.operators = operators
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        self.pos += 1

    def parse(self) -> Node:
        return self.parse_expression(0)

    def parse_primary(self) -> Node:
        token = self.current()
        if token is None:
            raise Exception('Unexpected end of input')
        if token == '(':
            self.consume()
            node = self.parse_expression(0)
            if self.current() != ')':
                raise Exception('Missing closing parenthesis')
            self.consume()  # Consume ')'
            return node
        # טיפול באופרטור חד־ערכי (prefix) – למשל, ~
        if token in self.operators and self.operators[token].arity == 1 and token not in ['!']:
            op = self.operators[token]
            self.consume()
            child = self.parse_expression(op.power)
            return UnaryOpNode(op, child)
        # צפוי מספר (כולל מספר עם מינוס כחלק מהליטרל)
        try:
            value = float(token)
            self.consume()
            return NumberNode(value)
        except ValueError:
            raise Exception(f'Invalid token: {token}')

    def parse_expression(self, precedence: int) -> Node:
        node = self.parse_primary()
        while self.current() and self.current() in self.operators:
            token = self.current()
            op = self.operators[token]
            if op.power < precedence:
                break
            self.consume()
            if op.arity == 1:
                node = UnaryOpNode(op, node)
            elif op.arity == 2:
                right = self.parse_primary()
                node = BinaryOpNode(op, node, right)
        return node

class Validation(ABC):
    def __init__(self, input_usr):
        if input_usr is None:
            raise Exception('input must be provided')
        self.input_usr = input_usr
        self.language_dict = {}

    def clean_spaces(self, iteration=0):
        if not isinstance(self.input_usr, str):
            pass
        if iteration == len(self.input_usr):
            return self.input_usr
        if self.input_usr[iteration] == ' ':
            self.input_usr = self.input_usr[:iteration] + self.input_usr[iteration + 1:]
        return self.clean_spaces(iteration + 1)

class LogicValidaion(Validation):
    def __init__(self, input_usr):
        super().__init__(input_usr)
        if not isinstance(input_usr, str):
            raise TypeError('input must be str')
        if self.check_logic() == False:
            raise Exception('Logic is not valid')

    def check_logic(self, iteration=0):
        if len(self.input_usr) == iteration:
            return True
        if (self.input_usr[iteration] not in self.language_dict
                and not self.input_usr[iteration].isdigit()
                and self.input_usr[iteration] != "."):
            return False
        return self.check_logic(iteration + 1)

class RoundBracketValidation(LogicValidaion):
    def __init__(self, input_usr):
        super().__init__(input_usr)
        if self.round_bracket_valid() == False:
            raise Exception('Round bracket validation failed')

    def round_bracket_valid(self, iteration=0, count=0):
        if len(self.input_usr) == iteration:
            return count == 0
        if self.input_usr[iteration] == '(':
            count += 1
        elif self.input_usr[iteration] == ')':
            count -= 1
            if count < 0:
                return False
        return self.round_bracket_valid(iteration + 1, count)

class InputLogicValidation(LogicValidaion):
    def __init__(self, input_usr):
        super().__init__(input_usr)

if __name__ == '__main__':
    calculator = MathOperation()

    expr1 = '~-5+90'  # ~(-5) = 5, ואז 5+90 = 95.
    expr2 = '~-10 + 4!'  # בתוך הסוגריים: -50+95*8 = 710; לאחר מכן: 710-20 = 690; ואז: 690+(~50) כאשר ~50 = -50 → 640.
    expr3 = '5!)'  # 5! = 120.0
   #### expr4 = '~-5!+10'  # יתפרש כ: ~ (5!) + 10 → 5! = 120, ~120 = -120, ואז -120+10 = -110.
    expr5 = '5.5/0'  # לדוגמה, עצרת 5.5 = gamma(6.5)

    print(f"Expression: {expr1} = {calculator.evaluate(expr1)}")
    print(f"Expression: {expr2} = {calculator.evaluate(expr2)}")
    print(f"Expression: {expr3} = {calculator.(expr3)}")
