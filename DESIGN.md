# Stack project design

Author: Emory Bruington

## Stack ADT

Stack() creates an empty LIFO collection. push(item) adds an item with no
precondition. pop() removes and returns the top item; peek() returns the top
without mutation. Both raise IndexError when empty and leave that state intact.
is_empty() returns a boolean; size() returns the number of stored items.
The backing Python list is private to Stack; client modules use its public API.

## Expression class contracts

InfixToPostfixConverter.convert(expression) accepts a string containing unsigned
integers or decimal literals, identifiers, binary + - * /, parentheses, and
whitespace. Output is a space-separated postfix string. Identifiers begin with
an ASCII letter or underscore, followed by ASCII letters, digits, or underscores.
Number literals use digits with an optional fractional part, or a leading decimal
point followed by digits. Scientific notation and unary signs are outside scope.
Whitespace between infix operators and operands is optional. A single operand
is valid. Adjacent operands and implicit multiplication are rejected.

PostfixEvaluator.evaluate(expression) accepts a whitespace-separated string of
unsigned integer/decimal operands and binary + - * /. Its result is an int or
float. Division uses Python's true division. Negative results are allowed;
unary signs on input operands are outside this contract. Exactly one value
must remain after processing. The evaluator does not resolve identifiers.

Both classes use a fresh Stack for every call. They raise TypeError for a
non-string argument, ValueError for invalid syntax or tokens, and the evaluator
raises ZeroDivisionError for a zero divisor. Non-finite numeric values/results
are rejected rather than returned as misleading answers.

## Conversion algorithm

Track whether an operand or an operator is expected. Every non-whitespace
character must be accounted for by tokenization. On an operand, output it.
Push opening parentheses. On a closing parenthesis, drain operators to the
matching opening parenthesis and discard the pair. For each binary operator,
pop stacked operators whose precedence is GREATER THAN OR EQUAL to its own,
then push it. At the end, reject incomplete syntax and drain the operator stack,
rejecting leftover parentheses. The official instructions' >= rule takes
precedence over the abbreviated background handout's > rule.

## Evaluation algorithm

Read numeric tokens left to right. Push operands. Before applying an operator,
require at least two items. Pop right first, then left. Apply left operator
right and push the result. Require exactly one result at completion.

## Module responsibilities and development order

1. stack.py: list-backed Stack plus direct assertion tests.
2. postfix_evaluator.py: numeric evaluation, validation, direct assertion tests.
3. infix_converter.py: shunting-yard conversion, token/syntax validation, direct tests.
4. main.py: imports the classes and presents integrated examples and handled errors.

Direct tests run only under __main__ guards. Imports produce no test output.
The practice worksheets supply reference cases; completing separate worksheet
submissions is not assumed. The official report template is needed before
report authoring, and it must be filled without changing its questions.

## Complexity and reliability

List-backed push/pop are amortized O(1); peek, size, and emptiness are O(1).
Conversion/evaluation are O(n) in token count under ordinary arithmetic-cost
assumptions, with O(n) worst-case auxiliary space. Tokenization is linear in
input characters; large-integer arithmetic costs depend on numeric magnitude.
Collect output tokens and join once. No eval, exec, fixed stack capacity,
or arbitrary expression-size limit is needed.

Malformed input is reported with clear exceptions. Integration handles only
expected input errors and continues with subsequent cases. Unexpected programming
errors must remain visible. Tests compare expected and actual values; printing
an example alone does not establish correctness.
