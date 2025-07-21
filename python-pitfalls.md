# First, working with uv when others are using venv and pip

## Stop using requirements.txt
requirements.txt is a very old format. pip has been able to use pyproject.toml for a long time with `pip install .`

uv uses pyproject.toml, as does modern pip and poetry and others.
Convert a requirements.txt to a modern pyproject.toml and .venv directory:
```
uv init --bare # creates pyproject.toml
uv add -r requirements.txt # convert to pyproject.toml
```

Now uv people keep woring using `uv run` and it will find the `pyproject.toml` and `.venv`
And pip/venv people keep working using `source .venv/bin/activate`

To add new libraries, uv people `uv add library`, pip people manually edit `pyproject.toml` and `pip install .`

Example:

```
$ uv init --bare
$ cat requirements.txt
requests
numpy
pandas
$ uv add -r requirements.txt
$ cat pyproject.toml
[project]
name = "my-project"
version = "0.1.0"
dependencies = [
    "requests>=2.31.0",
    "numpy>=1.26.4",
    "pandas>=2.2.2",
]
```

# Now for Python Pitfalls's:

## implicit string concatenation

```
t: str = ( 'this is a very long string '
           'so I split it up into '
           'several separate lines' )
print(t)
```

```
l: str = ['a', 'b', 'c' 'd', 'e', 'f'] # oooops
print(len(l), l)
```

Use `'hello '+'world'` instead of `'hello ' 'world'`

Use `t: str = f'I am {x} years old'`
instead of `t: str = 'I am '+str(x)+' years old'`

## Accidental Tuples

```
t = (1,2,3) # a simple tuple
t2 = 1,2,3 # another tuple... its not the (parens) its the commas that do it
not_t1 = (1) # just an int
t3 = 1, # this is a tuple! the comma makes it so
# but a typo could easily make an accidental tuple:
my_int = 1, # nope, it's a tuple
```

## for ... else, while ... else, try except finally else
Unlike if/else,
in for/else and while/else the else is only executed if the loop finished normally
It's a very unintuitive. Better to think of it as the "NO BREAK / NO EXCEPT" clause

```
for name in ['John', 'Sam', 'Peter', 'Gilberto', 'Massimo']:
  if name=='Peter':
    print('Peter is breaking things. The party is over.')
    break
  print(f'{name} is partying!')
else: # nobreak
  print('Everyone is partying!')
```

```
print('Commencing countdown, engines on')
i=10
while i>0:
  print(f'Countdown {i}')
  if i==5:
    print("your circuit's dead, theres something wrong")
    break
  i-=1
else: # nobreak
  print('Lift off!')
```

```
try:
  print('This is bad code')
  raise ValueError('Bad code')
except ValueError:
  print('Bad code handled')
else: # noexcept
  print('There were no errors')
```

## try/except/else/finally

```
try:
  print('try to run this risky code')
except ValueError:
  print('this runs to handle a ValueError exception'
else: # noexcept
  print('this runs if there was NO exception')
finally:
  print('this always runs even if there was an uncaught exception, a return(), a break, a continue, sys.exit() (but NOT os._exit()')
  print('clean-up goes here')

print('this runs after the try/except unless there was an uncaught exception or return()')
```

## except Exception
Don't blindly catch every exception. Catch exactly the one you expect next to the try block and catch anything else at the top of your program.

```
try:
  # lots of code
  r=a/b
  # lots more code
except Exception:
  print('we really dont know what went wrong')
```
better:
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
        print(f"Unhandled exception: {e}")
        put_details_in_log_file()
        send_alert_to_ops()
```

