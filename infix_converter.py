"""Convert infix expressions with the shunting-yard algorithm.
Author: Emory Bruington.
"""
import re
from stack import Stack


class InfixToPostfixConverter:
    """Convert identifiers/numbers and binary + - * / with parentheses.

    Whitespace is optional in infix input. Unary signs and implicit
    multiplication are not supported. Output tokens are separated by spaces.
    """
    _PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
    _NUMBER = r'(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)'
    _IDENTIFIER = r'[A-Za-z_][A-Za-z0-9_]*'
    _TOKEN = re.compile(r'\s+|' + _NUMBER + '|' + _IDENTIFIER + r'|[()+*/-]')
    _OPERAND = re.compile('(?:' + _NUMBER + '|' + _IDENTIFIER + ')')

    @staticmethod
    def _tokenize(expression):
        """Read every character; raise ValueError at an unrecognized character."""
        tokens = []
        position = 0
        while position < len(expression):
            match = InfixToPostfixConverter._TOKEN.match(expression, position)
            if match is None:
                raise ValueError(f'Invalid infix character {expression[position]!r} at position {position}.')
            token = match.group()
            if not token.isspace():
                tokens.append(token)
            position = match.end()
        return tokens

    def convert(self, expression):
        """Return a postfix string in O(n) token operations.

        Require a string of valid operands and binary operators. Raise
        TypeError for other input types and ValueError for invalid tokens,
        mismatched parentheses, misplaced tokens, or incomplete expressions.
        Each call owns its stack, so a failed call cannot affect another call.
        """
        if not isinstance(expression, str):
            raise TypeError('Infix expression must be a string.')
        tokens = self._tokenize(expression)
        if not tokens:
            raise ValueError('Infix expression is empty.')
        operators = Stack()
        output = []
        expect_operand = True
        for token in tokens:
            if self._OPERAND.fullmatch(token):
                if not expect_operand:
                    raise ValueError(f'Misplaced operand {token!r}; an operator is required.')
                output.append(token)
                expect_operand = False
            elif token == '(':
                if not expect_operand:
                    raise ValueError('An operator is required before an opening parenthesis.')
                operators.push(token)
            elif token == ')':
                if expect_operand:
                    raise ValueError('Missing operand before a closing parenthesis.')
                while not operators.is_empty() and operators.peek() != '(':
                    output.append(operators.pop())
                if operators.is_empty():
                    raise ValueError('Mismatched parentheses: no opening parenthesis.')
                operators.pop()
                expect_operand = False
            else:
                if expect_operand:
                    raise ValueError(f'Misplaced operator {token!r}; an operand is required.')
                # Equal precedence must pop too because every operator is left-associative.
                while (not operators.is_empty()
                       and operators.peek() in self._PRECEDENCE
                       and self._PRECEDENCE[operators.peek()] >= self._PRECEDENCE[token]):
                    output.append(operators.pop())
                operators.push(token)
                expect_operand = True
        if expect_operand:
            raise ValueError('Incomplete infix expression: an operand is required at the end.')
        while not operators.is_empty():
            token = operators.pop()
            if token == '(':
                raise ValueError('Mismatched parentheses: no closing parenthesis.')
            output.append(token)
        return ' '.join(output)


def _run_tests():
    """Run worksheet conversions, associativity cases, and malformed inputs."""
    converter = InfixToPostfixConverter()
    valid = [
        ('A + B', 'A B +'), ('A + B * C', 'A B C * +'),
        ('(A + B) * C', 'A B + C *'), ('A * B + C / D', 'A B * C D / +'),
        ('(A + B) * (C - D)', 'A B + C D - *'),
        ('A + B * C - D / E', 'A B C * + D E / -'),
        ('A * (B + C) / D', 'A B C + * D /'),
        ('(A + B * C) / (D - E)', 'A B C * + D E - /'),
        ('A + (B - C) * D', 'A B C - D * +'),
        ('(A + B * (C - D)) / E', 'A B C D - * + E /'),
        ('A - B + C', 'A B - C +'), ('A / B * C', 'A B / C *'),
        ('A - (B - C)', 'A B C - -'), ('A/B/C', 'A B / C /'),
        ('(((((((( A + B ))))))))', 'A B +'),
        ('(' * 64 + 'A+B' + ')' * 64, 'A B +'),
        ('A', 'A'), ('42', '42'), ('((A))', 'A'),
        ('12.5+3*4', '12.5 3 4 * +'), ('.5 + 2', '.5 2 +'),
        ('A1 + B_2 * _value', 'A1 B_2 _value * +'),
        ('\tA\n+\tB ', 'A B +'),
    ]
    count = 0
    for expression, expected in valid:
        actual = converter.convert(expression)
        assert actual == expected, (expression, expected, actual)
        count += 1
    invalid = [
        'A + B ) C', 'A + B ; C', '+ A B', 'A + * B', 'A B + C',
        'A + ) B * C (', '( A + B', 'A + B )', '', '   ', 'A +', '()',
        'A + B @ C', 'A + B /', 'A(B+C)', '(A)(B)', '(A)B',
        '-A+B', 'A+-B', 'A++B', 'A^B', '12A+B', '1.2.3+4',
        'A+()', '(( ))', 'A+B$C',
    ]
    for expression in invalid:
        try:
            converter.convert(expression)
        except ValueError as error:
            assert str(error)
        else:
            raise AssertionError(f'Expected ValueError for {expression!r}.')
        assert converter.convert('A+B') == 'A B +'
        count += 1
    for expression in (None, 42):
        try:
            converter.convert(expression)
        except TypeError:
            pass
        else:
            raise AssertionError('Non-string input did not raise TypeError.')
        count += 1
    assert converter.convert('A+B*C-D/E+F') == 'A B C * + D E / - F +'
    count += 1
    print(f'InfixToPostfixConverter: all {count} test cases passed.')


if __name__ == '__main__':
    _run_tests()
