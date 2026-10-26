# Stack Project Infix and Postfix Expressions

Author: Emory Bruington

This project uses a list-backed Stack ADT to convert infix expressions with the
shunting-yard algorithm and to evaluate numeric postfix expressions. Each class
owns its work and reports malformed input with meaningful exceptions.

## Run

Python 3.12 was used for verification. No third-party packages are required.
From this folder:

```console
python stack.py
python postfix_evaluator.py
python infix_converter.py
python main.py
```

The first three commands run assertion tests behind __main__ guards. Importing
these modules does not print output or run their tests. main.py demonstrates
both classes and handles expected input errors.

## Input contracts

Infix accepts ASCII identifiers, unsigned integers/decimals, binary + - * /,
parentheses and optional whitespace. Identifiers begin with a letter or
underscore and may continue with letters, digits or underscores. Decimal
literals can be 12.5 or .5. Unary signs, exponent notation and implicit
multiplication are outside scope. A single operand is valid.

Postfix requires whitespace-separated unsigned numeric literals and the same
four binary operators. It does not resolve variable names. Division uses true
division; negative computed results are valid. Invalid expressions raise
ValueError, division by zero raises ZeroDivisionError, and non-string inputs
raise TypeError. Empty Stack pop/peek raise IndexError. Non-finite numeric
values/results are rejected. A fresh working stack makes repeated calls safe.

## Modules and evidence

- stack.py: Stack plus 10 direct test cases.
- postfix_evaluator.py: evaluator plus 44 direct test cases.
- infix_converter.py: converter plus 52 direct test cases.
- main.py: 16 lines of integrated normal and handled-error output.
- DESIGN.md and PSEUDOCODE.md: contracts, algorithms and complexity.
- evidence/: actual module and integration output.
- study_materials/: original instructor documents and a future study plan.

Additional integration verification compared 200 generated expressions with
independent rational arithmetic. See evidence/integration-results.txt.

## Visual Studio

Open StackProject.pyproj with the Python development workload installed. Select
a compatible Python environment, then run the module you want to check or use
Debug > Execute Project in Python Interactive. main.py is the normal startup file.
Start Without Debugging (Ctrl+F5) and Python Interactive were verified in Visual
Studio Community 2026 with the project Python 3.12 environment. See evidence/
visual-studio-main.png and visual-studio-verification.txt.
Local interpreter settings belong in the ignored StackProject.pyproj.user file;
no machine-specific interpreter path is included in the portable project.

F5 debugging was also verified. Its 16-line output exactly matched the expected
demonstration output; see evidence/visual-studio-debug-output.txt.
All 106 direct module test cases also passed in the project Python Interactive
window (Stack: 10; evaluator: 44; converter: 52).
