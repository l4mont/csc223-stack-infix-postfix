# Stack project pseudocode

Author: Emory Bruington

## Stack

PUSH(item): append item to the private list.
POP(): if empty, raise IndexError; otherwise remove and return the last item.
PEEK(): if empty, raise IndexError; otherwise return the last item unchanged.
IS_EMPTY(): return whether the private list is empty.
SIZE(): return the private list length.

The most recently pushed item is the first removed. Clients use these operations
rather than accessing the backing list. Push/pop are amortized O(1); the other
operations are O(1).

## Tokenization

Require a string. Start at position zero. At each position, match whitespace,
a supported number, an identifier, or one of the operators/parentheses. Reject
an unrecognized character at its actual position. Save non-whitespace tokens
and continue at the end of the match. No characters may be silently skipped.

## Infix conversion

```text
create empty operator Stack and output sequence
expect_operand = True
for token in input tokens:
    if token is an operand:
        if not expect_operand: raise ValueError
        add token to output
        expect_operand = False
    else if token is '(':
        if not expect_operand: raise ValueError
        push '(' onto operators
    else if token is ')':
        if expect_operand: raise ValueError
        while operators is nonempty and top is not '(':
            move top operator to output
        if operators is empty: raise ValueError
        discard matching '('
        expect_operand = False
    else:  # binary operator
        if expect_operand: raise ValueError
        while top is an operator with precedence >= current token:
            move top operator to output
        push current operator
        expect_operand = True
if input was empty or expect_operand: raise ValueError
while operators is nonempty:
    pop token
    if token is '(': raise ValueError
    add token to output
return output joined with single spaces
```

The >= comparison preserves left associativity. For A - B + C, subtraction
must reach the output before addition. Parentheses protect their internal
operators until the matching closing parenthesis is processed.

## Postfix evaluation

```text
require a nonempty string of whitespace-separated tokens
create empty operand Stack
for token in input tokens:
    if token is an operator:
        if operand count < 2: raise ValueError
        right = pop operand
        left = pop operand
        if operator is '/' and right == 0: raise ZeroDivisionError
        result = left operator right
        reject overflow or a non-finite result
        push result
    else:
        validate unsigned numeric token
        convert to int or finite float
        push value
if operand count != 1: raise ValueError
return pop operand
```

Popping right before left matters: 8 2 - means 8 - 2, not 2 - 8. An extra value
at completion means some input was never combined into the final expression.

Conversion and evaluation perform O(n) token operations with O(n) worst-case
space, assuming ordinary arithmetic costs. Every token is handled once and each
operator is pushed/popped at most once. Tokenization also scans input characters
linearly. Arbitrary-precision arithmetic has additional magnitude-dependent cost.
