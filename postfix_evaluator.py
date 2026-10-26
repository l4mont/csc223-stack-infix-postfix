"""Evaluate numeric postfix expressions using Stack. Author: Emory Bruington."""
import math
import re
from stack import Stack


class PostfixEvaluator:
    """Evaluate space-separated unsigned numbers and binary +, -, *, /.

    Each call uses a fresh stack. Results may be negative; unary signs and
    variable names are outside the input contract. Division returns a float.
    """
    _NUMBER = re.compile(r'(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)')
    _OPERATORS = frozenset('+-*/')

    @staticmethod
    def _parse_number(token):
        """Return an int/finite float, or raise ValueError for an invalid token."""
        if PostfixEvaluator._NUMBER.fullmatch(token) is None:
            raise ValueError(f'Invalid postfix token: {token!r}.')
        try:
            value = float(token) if '.' in token else int(token)
        except ValueError as error:
            raise ValueError(f'Unsupported numeric value: {token!r}.') from error
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError('Numeric operands must be finite.')
        return value

    @staticmethod
    def _apply_operator(operator, left, right):
        """Apply left operator right; reject zero divisors and non-finite results."""
        try:
            if operator == '+':
                result = left + right
            elif operator == '-':
                result = left - right
            elif operator == '*':
                result = left * right
            elif operator == '/':
                if right == 0:
                    raise ZeroDivisionError('Cannot divide by zero.')
                result = left / right
            else:
                raise ValueError(f'Unsupported operator: {operator!r}.')
        except OverflowError as error:
            raise ValueError('Arithmetic result is outside the supported numeric range.') from error
        if isinstance(result, float) and not math.isfinite(result):
            raise ValueError('Arithmetic result must be finite.')
        return result

    def evaluate(self, expression):
        """Return one numeric result in O(n) token operations.

        Require a string of whitespace-separated tokens. Raise TypeError for
        other input types, ValueError for invalid syntax, and ZeroDivisionError
        for a zero divisor. Failed calls leave no persistent operand state.
        """
        if not isinstance(expression, str):
            raise TypeError('Postfix expression must be a string.')
        tokens = expression.split()
        if not tokens:
            raise ValueError('Postfix expression is empty.')
        operands = Stack()
        for token in tokens:
            if token in self._OPERATORS:
                if operands.size() < 2:
                    raise ValueError(f'Insufficient operands for operator {token!r}.')
                right = operands.pop()
                left = operands.pop()
                operands.push(self._apply_operator(token, left, right))
            else:
                operands.push(self._parse_number(token))
        if operands.size() != 1:
            raise ValueError('Postfix expression has extra operands; one result is required.')
        return operands.pop()


def _run_tests():
    """Run the instruction/worksheet cases and additional boundary checks."""
    evaluator = PostfixEvaluator()
    valid = [
        ('5 3 +', 8), ('8 2 - 3 +', 9), ('5 3 8 * +', 29),
        ('6 2 / 3 +', 6.0), ('5 8 + 3 -', 10), ('5 3 + 8 *', 64),
        ('8 2 3 * + 6 -', 8), ('5 3 8 * + 2 /', 14.5),
        ('8 2 + 3 6 * -', -8), ('5 3 + 8 2 / -', 4.0),
        ('35 27 + 3 *', 186), ('23 30 15 * /', 23 / 450),
        ('8 2 -', 6), ('8 2 /', 4.0), ('2 8 -', -6), ('2 8 /', .25),
        ('42', 42), ('0', 0), ('.5 1.25 +', 1.75),
        ('  12\t3\n/  ', 4.0), ('3 8 - 2 *', -10),
    ]
    count = 0
    for expression, expected in valid:
        actual = evaluator.evaluate(expression)
        assert math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12), (expression, actual)
        count += 1
    invalid = [
        ('', ValueError), ('   ', ValueError),
        ('26 28 + 32 2 ; - 5 /', ValueError), ('2 3 4 +', ValueError),
        ('20 29 9 * ;', ValueError), ('25 23 - +', ValueError),
        ('8 0 /', ZeroDivisionError), ('5 +', ValueError), ('3 + 4', ValueError),
        ('3 4 &', ValueError), ('1 2', ValueError), ('A B +', ValueError),
        ('-2 3 +', ValueError), ('( 2 )', ValueError), ('nan', ValueError),
        ('inf', ValueError), ('1e3', ValueError), ('1.2.3', ValueError),
        ('8 1 1 - /', ZeroDivisionError), (None, TypeError), (42, TypeError),
        ('9' * 400 + '.0', ValueError),
    ]
    for expression, error_type in invalid:
        try:
            evaluator.evaluate(expression)
        except error_type as error:
            assert str(error)
        else:
            raise AssertionError(f'Expected {error_type.__name__} for {expression!r}.')
        # A failed expression must not contaminate a subsequent call.
        assert evaluator.evaluate('5 3 +') == 8
        count += 1
    assert evaluator.evaluate('1 2 + 3 + 4 +') == 10
    count += 1
    print(f'PostfixEvaluator: all {count} test cases passed.')


if __name__ == '__main__':
    _run_tests()
