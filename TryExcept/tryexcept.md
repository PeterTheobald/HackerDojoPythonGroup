# Exception Handling in Python

## The old way

There are two ways to handle unexpected events or responses in most languages.

1. Return a special "sentinel" value (None, -1, a unique object, "", 0, etc)
2. "Raise" or "Throw" an exception to be caught and handled.

The older way used in C was to return a special value that wouldn't normally returned. So a function that returns positive integers might return -1 to signal an error. The specific error would be set in a global variable 'errno'. 

This worked but has a number of downsides:
- You had to find a value that couldn't normally be returned. What if -1 or "" or 0 are valid return values?
- The specific error had to be communicated another way, for example in a global variable
- If the error happened deep in nested code you would need many levels of if/then to get out

Here's an example of a Python module that uses a return value to signal an error:
``` python
import os

cmd = "ls"
ret = os.system( cmd)
if ret != 0:
  print(f'Error executing command: error number {ret}')

cmd = "non-existent-command"
ret = os.system( cmd)
if ret != 0:
  print(f'Error executing command: error number {ret}')
```

Here is an example of needing to escape from deep in nested code:
``` python
err=False
for i in range(5):
    if err: break # exit outer loop
    for j in range(5):
        val, success = do_task(i,j)
        if not success:
            error = True
            break  # exit inner loop
```

## The modern way

A better way is to have a way to handle exceptions that interrupts the normal flow of the program. Python introduced "try/except" blocks for this. Most modern languages since C have support for exception handling with try/except blocks. (Javascript calls it try/catch)

The basic syntax is:
``` python
try:
  # risky code
except SomeException:
  # handle the error
```

Here is the same code from above using try/except:
``` python
try:
    for i in range(5):
        for j in range(5):
            val=do_task(i,j)
except ValueError as e:
    print(f'Error: {e}')
```

The Go language is a notable modern exception that requires you to return two values for error handling:
``` go
val, err := someFunction()
if err != nil {
    // handle error
}
```
Go-lang doesn't have try/except. It uses a very different way of handling errors with deferred function calls for cleanup.

You can catch specific exceptions:
``` python
try:
    x = 1 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
```

You can catch multiple exceptions:
``` python
try:
    risky_function()
except (TypeError, ValueError) as e:
    print(f"Handled error: {e}")
```

## Bubbling up...

Any exceptions you don't specifically catch will exit the function and check if the calling function catches it, and if not that function's calling function and so on all the way up the stack to your main program.
It is a best practice to catch the most specific error you can in your try/except block and have a broad general purpose try/except in your main function for any uncaught exceptions.

This program catches specific expected errors, and uses a broad general purpose try/except in the main function:
``` python
def inner():
    try:
        x = int("abc")  # raises ValueError
    except ValueError:
        print("inner: caught ValueError")

    y = undefined_var  # NameError, not in try block

def middle():
    try:
        inner()
    except NameError:
        print("middle: caught NameError")

def main():
    try:
        middle()
    except Exception as e:
        print(f"main: caught unhandled exception: {e}")

main()
```

## Exception objects

The exceptions that you can catch come from a list of standard Python exceptions that are all objects inherited from the parent Exception object. You can find a list of all the built-in exceptions here: https://docs.python.org/3/library/exceptions.html
Exception objects have a number of attributes on them that give you additional information about the exception.

You can create your own custom application specific exceptions by creating an object that inherits from Exception:
``` python
class NoNegativesAllowedInThisFamily(Exception):
    pass

def do_something(x):
    if x < 0:
        raise NoNegativesAllowedInThisFamily("Negative value not allowed")
    return x * 2

try:
    result = do_something(-1)
except NoNegativesAllowedInThisFamily as e:
    print(f"Caught custom exception: {e}")
```

You can see I used the statement 'raise' to create an exception manually. You can use 'raise' to raise any standard or custom exceptions. It is often used when you want to handle an exception but also pass it up the calling stack to continue being handled by a calling function.

``` python
class DatabaseConnectionError(Exception):
    pass

def connect_to_db():
    try:
        # Simulate connection failure
        raise DatabaseConnectionError("Could not connect to DB")
    except DatabaseConnectionError as e:
        print("connect_to_db: logging connection failure")
        raise  # propagate to caller for higher-level handling

def fetch_data():
    try:
        connect_to_db()
    except DatabaseConnectionError as e:
        print(f"fetch_data: returning cached data due to error: {e}")

fetch_data()
```

You can raise standard Python errors. For example, KeyError is often used for dict keys that don't exist, but you can use it when a key doesn't exist in your database:
``` python
def get_user_age(data, user_id):
    if user_id not in data:
        raise KeyError(f"User ID {user_id} not found")
    age = data[user_id].get("age")
    if age is None:
        raise ValueError(f"Age not available for user {user_id}")
    return age

users = {
    1: {"name": "Alice", "age": 30},
    2: {"name": "Bob"}  # Missing age
}

try:
    age = get_user_age(users, 2)
except (KeyError, ValueError) as e:
    print(f"Error retrieving user age: {e}")
```

You can use `raise` by itself to re-raise the current exception to the caller:
``` python
try:
    # dangerous code
except ValueError:
    log_error()
    raise  # re-raises the same exception
```

## try except else finally

Python exception handling also has an "else" and "finally" block for executing code after an exception is handled. They can be confusing. The 'except' block is only run if there is an error/exception. The 'else' block is only run if there was NO exception. The 'finally' block is always run after the try/except blocks EVEN IF THE try/except blocks caused an uncaught exception or the function exitted with `return` or the try/except/finally block was skipped by a `break` or `continue` or even if the program was aborted with `sys.exit()`. 'finally' ALWAYS RUNS. Any code placed after the entire try/except will run afterwards unless there the function aborted with an uncaught exception or a return.

``` python
try:
  print('try to run this risky code')
except ValueError:
  print('this runs to handle a ValueError exception')
else: # noexcept
  print('this runs if there was NO exception')
finally:
  print('this always runs even if there was an uncaught exception, a return(), a break, a continue, sys.exit() (but NOT os._exit()')
  print('clean-up goes here')

print('this runs after the try/except unless there was an uncaught exception or return()')
```

## Pythonic exception handling

Most other languages prefer to use try/except only for errors. Python encourages using try/except for any sort of out of the normal flow. Use it to handle any non-happy path:
``` python
def parse_int(value):
    try:
        return int(value)
    except ValueError:
        return None

user_input = "123"  # string! could also be "abc"

parsed = parse_int(user_input)
if parsed is not None:
    print(f"Parsed integer: {parsed}")
else:
    print("Invalid input: not an integer")
```

Python uses this itself in the implementation of Iterators. Python iteration raises StopIteration to signal the end of a sequence. This is how `for` loops work under the hood. Here is a custom iterator; See how it raises a StopIteration exception to signal the end of the sequence:
``` python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self  # the iterator object

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

# Usage
for number in Countdown(3):
    print(number)
```

Python uses `assert` and `AssertionError` as debugging tools:
``` python
assert x > 0, "x must be positive"
```

## Detailed exception information

You can get lots of detailed information about an exception to print or log very helpful messages. This can be especially useful if your exception bubbled up more than one caller in the stack before being caught and printed, making it not obvious where the exception happened.

``` python
import traceback
import sys

def fail():
    raise ValueError("Something went wrong")

try:
    fail()
except Exception:
    exc_type, exc_value, exc_tb = sys.exc_info()
    tb = traceback.extract_tb(exc_tb)
    last_call = tb[-1]
    print(f"Exception in function '{last_call.name}' on line {last_call.lineno}")
```

Or even print an entire stack trace from where the error happened:
``` python
import traceback

def fail():
    raise ValueError("Something went wrong")

try:
    fail()
except Exception:
    traceback.print_exc()
```

## best practices

- Try to keep the least code possible in the try block, only the dangerous code.
- Don't blindly catch every exception. Catch exactly the one you expect in the try block and catch anything else at the top of your program.
- Put a broad general purpose try/except around your main function for any other uncaught exceptions
- In production systems it's best to log exceptions instead of just printing
``` python
try:
  # lots of code
  r=a/b
  # lots more code
except Exception:
  print('we really dont know what went wrong')
```
Better:
```
try:
  r=a/b
except ZeroDivisionError:
  print('we handle if b was zero here')

# and at the very top level of your program
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        send_alert_to_ops()
```


