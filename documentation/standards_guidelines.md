# CODING STANDARS AND GUIDELINES

## Code layout

### Indentation

Use 4 spaces per indentation level.

Continuation lines should align wrapped elements either vertically using Python's implicit line joining inside parentheses, brackets and braces, or using a hanging indent. When using a hanging indent the following should be considered; there should be no arguments on the first line and further indentation should be used to clearly distinguish itself as a continuation line:

```python
# Aligned with opening delimiter.
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# Add 4 spaces (an extra level of indentation) to distinguish arguments from the rest.
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# Hanging indents should add a level.
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)

```

The closing brace/bracket/parenthesis on multiline constructs may be lined up under the first character of the line that starts the multiline construct, as in:


```python
my_list = [
    1, 2, 3,
    4, 5, 6,
]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
)
```

### Max line length
Backslashes may still be appropriate at times. For example, long, multiple with-statements cannot use implicit continuation, so backslashes are acceptable

```python
with open('/path/to/some/file/you/want/to/read') as file_1, \
     open('/path/to/some/file/being/written', 'w') as file_2:
    file_2.write(file_1.read())
```

### Source File Encoding
Use *UTF-8* for the code

### Imports
Imports should be on separated lines

```python
import os
import sys
```

For multiple import from a same module, could be on the same line:
```python
from subprocess import Popen, PIPE
```

Imports are always put at the top of the file, just after any module comments and docstring, and before module globals and constants.

Imports should be grouped in the following order:

1. Standard library imports.
2. Related third party imports.
3. Local application/library specific imports.

You should put a blank line between each group of imports.

Absolute imports are recommended, as they are usually more readable and tend to be better behaved. However, explicit relative imports are an acceptable alternative to absolute imports, especially when dealing with complex package layouts where using absolute imports would be unnecessarily verbose:

```python
from . import sibling
from .sibling import example
```

Wildcard imports should be avoided `from <module> import *`

### Whitespace in expressions and statements

Avoid extraneous whitespace in the following situations

```python
# Correct:
spam(ham[1], {eggs: 2})

# Wrong:
spam( ham[ 1 ], { eggs: 2 } )
```

Immediately before a comma, semicolon, or colon

```python
# Correct:
if x == 4: print x, y; x, y = y, x

# Wrong:
if x == 4 : print x , y ; x , y = y , x
```

## Comments

Comments that contradict the code are worse than no comments. Always make a priority of keeping the comments up-to-date when the code changes!

Comments should be complete sentences. The first word should be capitalized, unless it is an identifier that begins with a lower case letter (never alter the case of identifiers!).

All comments should be written in English

### Documentation strings

Write docstrings for all public modules, functions, classes, and methods. Docstrings are not necessary for non-public methods, but you should have a comment that describes what the method does. This comment should appear after the def line.

For consistency, always use """triple double quotes""" around docstrings. Use r"""raw triple double quotes""" if you use any backslashes in your docstrings. For Unicode docstrings, use u"""Unicode triple-quoted strings""".

#### One-line Docstring

One-liners are for really obvious cases. They should really fit on one line. For example

```python
def kos_root():
    """Return the pathname of the KOS root directory."""
    global _kos_root
    if _kos_root: return _kos_root
    ...

```

### Multi-line docstrings

Multi-line docstrings consist of a summary line just like a one-line docstring, followed by a blank line, followed by a more elaborate description. The summary line may be used by automatic indexing tools; it is important that it fits on one line and is separated from the rest of the docstring by a blank line. The summary line may be on the same line as the opening quotes or on the next line. The entire docstring is indented the same as the quotes at its first line 

For methods and functions, the documentation should had a short summary of what the function do. After the summary the documentation should describe every arguments of the functions, specifing the data type and the return value (as possible).

```python
def sum_natural_numbers(a: int, b: int) -> int:
    """ Sum two integers

    Args:
        a (int): First number
        b (int): Second number

    Raises:
        NotNaturalNumberException: An input number is not a natural number

    Returns:
        int: The result of sum the numbers
    """
    if a < 0 or b < 0:
        raise NotNaturalNumberException("The numbers couldn't be less than zero")
    return a + b
```

For more info about documentation via this link [Python Google Documentation](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings)

In order to made this documentation in the easiest way, it recommended to install an extension which use the Google's formats documentation style. In vscode there is an [extension](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) as well

## Project organization

This is a flask project, so the folder organization take importance. This project is an API in essence, so the folder organization is suggested at follow section.

* /
  * code/
    * tests/
    * api/
      * app/
        * Controllers/
        * Core/
            * Controllers/
            * Data/
            * Middlewares/
            * Services/
        * Data/
            * Enum/
            * Interfaces/
            * Models/
        * Exceptions/
        * Middlewares/
        * Services/
      * config/
      * database/
      * routes/
      * static/
      * storage/
      * templates/
      * utils/
      * `__init__.py`
    * .env
    * Environment.py
    * requirements.txt
    * Dockerfile.dev
    * odbcinst.ini
  * documentation/

## Git strategy

For Git, we'll use GitFlow Workflow metodology. This metodology split software production in many stages, and these stage will be git repository branches. This branches will be:

* __master/main__: Is the principal branch. In this one, should be the stable version of software
* __develop__: This is  the for development purpose, from this checkout any feature or bugfix, and to this will have been merge. To this one any change will be integrated
* __feature__: Every enhancement, feature or new component, should do in a feature prefix branch. This branch comes out from develop and its named with feature prefix and name of the feature. Ex. `feature/country_endpoints`
* __bugfix__: In case, in dev test part, the test team found a bug, this bug should be fixed in bugfix prefix branch. `bugfix/country_not_match`. This branch comes out from develop
* __hotfix__: If a bug is found in production, this one should be fixed in hotfix branch. This branch comes out from main. Ex: `hotfix/country_not_found`
* __release__: For every type of release like stagging, dev, UAT, etc. It should be with this prefix. This branch merge from develop. Ex: `release/UAT`

![image](documentation/images/gitflow.svg)

## Debug

For debug information in this [link](documentation/vscode_flask_debuger.md)



## Environment variables

The environment variables should be placed in the file: `code/.env`

For get access to `.env` file, please contact with dev team.
