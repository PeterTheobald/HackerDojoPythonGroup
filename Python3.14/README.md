Python 3.14 (or πthon)

- Better error messages
```
improt math
```

- Speed improvements
  [by Python version](https://lost.co.nz/articles/sixteen-years-of-python-performance/)
  [vs PyPy NodeJS Rust](https://blog.miguelgrinberg.com/post/is-python-really-that-slow)
  experimental JIT in 3.13 ~~ 1.4x speedup
  multithreading
  note: 3.13t is slower than 3.13 on non-threaded tasks

- Python debugger
  `python -m pdb --pid 49611`

- Syntax coloring in REPL
```
def compound( amount, interest, years):
  """Return amount after years of compounding interest."""
  for _ in range(years):
    amount *= 1+interest
  return amount
```

```
echo '[{"id":100, "name":"Peter", "is_admin":true}]' | uv run --python 3.14 python -m json
```

- TAB completion in REPL
```
import<TAB>
```

- Template Strings
Similar to f-strings, but defers interpolation of variables or expressions until after your custom processing function
gets to handle each interpolated expression.

Write your own custom handler, or use already made ones for SQL, HTML, etc.

```
product: str = "widget"
price: float = 10.5
discount: float = 0.15
msg = f"The product is {product} and the sale price is ${price-price*discount:.2f}"
print(msg)
type(msg)

product: str = "widget"
price: float = 10.5
discount: float = 0.15
template: Template = t"The product is {product} and the sale price is ${price-price*discount:.2f}"
print(template)
type(template)

print(list(template))
print(template.strings)
print(template.interpolations)
print(template.values)
type(template)

# simplest renderer:
from string.templatelib import Template
def render_simple( template: Template) -> str:
  values = []
  for part in template:
    if isinstance(part, str):
      values.append(part)
    else:
      values.append(str(part.value))
  return ''.join(values)

template: Template = t"The product is {product} and the sale price is ${price-price*discount}"
print(render_simple(template))

# better renderer, with formats:
def render_format( template: Template) -> str:
  values = []
  for part in template:
    if isinstance(part, str):
      values.append(part)
    else:
      val = format(part.value, part.format_spec or "")
      values.append(val)
  return ''.join(values)

# renderer to encode URLS
import urllib.parse
def render_URL( template: Template) -> str:
  values = []
  for part in template:
    if isinstance(part, str):
      values.append(part)
    else:
      val = urllib.parse.quote(str(part.value))
      values.append(val)
  return ''.join(values)

arg: str = "This is a string"
template: Template = t"http://www.google.com/?q={arg}"
print( render_URL(template))

# renderer to escape dangerous HTML
import html
def render_HTML( template: Template) -> str:
  values = []
  for part in template:
    if isinstance(part, str):
      values.append(part)
    else:
      val = html.escape(str(part.value))
      values.append(val)
  return ''.join(values)

evil_name: str = "Peter <script>alert('do bad things')</script>"
template: Template = t"<p>Hello, {evil_name}</p>"
print( render_HTML(template))


```

## why?
- security (injection attacks)
- DSL domain specific languages, special templates for HTML, SQL, 
- type checking in templates
- special handling, like redact sensitive information from logging before saving it

```

