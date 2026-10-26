"""Demonstrate the stack expression classes. Author: Emory Bruington."""
from infix_converter import InfixToPostfixConverter
from postfix_evaluator import PostfixEvaluator


def main():
    evaluator = PostfixEvaluator()
    converter = InfixToPostfixConverter()
    print('----- Postfix Evaluator -----')
    for expression in ('5 3 +', '8 2 - 3 +', '35 27 + 3 *', '5 3 8 * + 2 /',
                       '8 0 /', '2 3 4 +'):
        try:
            print(f'[{expression}] = {evaluator.evaluate(expression)}')
        except (ValueError, ZeroDivisionError) as error:
            print(f'[{expression}] -> ERROR: {error}')
    print('----- Infix to Postfix Converter -----')
    for expression in ('A + B', 'A + B * C', '(A + B) * C', 'A - B + C',
                       'A + * B', '( A + B'):
        try:
            print(f'[{expression}] -> [{converter.convert(expression)}]')
        except ValueError as error:
            print(f'[{expression}] -> ERROR: {error}')
    print('----- Convert and Evaluate -----')
    expression = '12 + 3 * (4 - 2)'
    postfix = converter.convert(expression)
    print(f'[{expression}] -> [{postfix}] = {evaluator.evaluate(postfix)}')


if __name__ == '__main__':
    main()
