# Error Handling in Python

**Best practices, trade-offs, and how Python differs from Go, C++, and other languages**

Python error handling model: "Easier to Ask Forgiveness than Permission"
Exception handling is built into the language.
- try the operation
- catch exceptions if it fails

Do this:
```
try:
    value = d["key"]
except KeyError:
    value = None
```
Instead of  this:
```
if "key" in d:
    value = d["key"]
else:
    value = None
```

Python exception handling is easy and efficient. It's so much preferred in Python control flow
that it is even used for normal functions to return exceptional results:
`str.index() raises ValueError if not found`

try/except is especially useful for things that can cause race conditions:
```
from pathlib import Path

path = Path("example.txt")

try:
    with path.open("x") as f:         # 'x'clusive fails if the file exists
        f.write("created new file\n")
except FileExistsError:
    with path.open("a") as f:
        f.write("appended: file already existed\n")
```
Better than this:
```
from pathlib import Path

path = Path("example.txt")

if not path.exists():
    # race condition: another process could create the file right here
    with path.open("w") as f:         # 'w' will overwrite any previous contents
        f.write("created new file\n")
else:
    with path.open("a") as f:
        f.write("appended: file already existed\n")
```



Other languages:
- Older languages like C, C++ check the return value for special error values.
    - This can be a problem when the special value may be a valid but unusual value like -1
    - This may affect the type of the return value: int|None
- GoLang functions always return TWO values (a tuple): the actual value and an error indicator


## Key questions

- When should Python raise exceptions vs return values?
- What makes exception handling maintainable at scale?
- Why do the same failure paths look so different in Go and C++?

---

## Roadmap

1. Python mental model  
   exceptions as control flow for failure, not for normal branching
2. Best practices  
   catch narrowly, preserve context, clean up reliably, design good exception types
3. Compare to Go, C++, plus quick notes on Java/C# and Rust
4. Code review checklist  
   what to keep, what to delete, what to test

Goal:
- Handle specific errors close to the source if possible.
- Bubble up unexpected bugs to a "main" error handler at the top of your program.
- Don't hide errors by "swallowing" them.

---


### Clean Happy Path

Prefer the happy path (success) to read cleanly. Let operations fail when they truly cannot proceed, then handle failures at the right boundary.
```
# Clean happy path: do the operation, handle only the failure case.
try:
    with open("config.json", "x") as f:
        f.write("{}")
except FileExistsError:
    # handle error...
```
```
# Less clean happy path: the main path is wrapped in a pre-check.
from pathlib import Path

path = Path("config.json")

if not path.exists():
    with path.open("w") as f:
        f.write("{}")
else:
    # handle error...
```

### User-facing messages vs. internal exceptions
- Internal Exceptions: handle as close to the error as possible, with lots of details (stack trace, bad values etc), bubble up unexpected errors to a main handler, log for debugging
- User-facing messages: send message to be presented on your user interface, give friendly clear description, give instructions on how to proceed
```
try:
    user = repo.load_user(user_id)
except DatabaseTimeoutError as e:
    logger.exception("Database timeout loading user %s", user_id)
    raise ServiceUnavailable("Please try again later") from e
```

---

## Core best practices in Python

Many production issues come from just a few exception-handling mistakes.

### Catch narrowly

Prefer specific exceptions over `except Exception:`. Handle only failures you know how to recover from.
```
# Good: catches only the error it expects and can recover from.
try:
    port = int(config["port"])
except KeyError:
    port = 8080
except ValueError:
    port = 8080
```
```
# Bad: catches everything, including unrelated bugs.
try:
    port = int(config["port"])
except Exception:
    port = 8080
```

### Preserve context

Use `raise` to rethrow and `raise ... from e` to translate while keeping causal history.
```
# Use `raise` to rethrow the same exception after logging or cleanup.
def load_user(user_id):
    try:
        return db.fetch_user(user_id)
    except DatabaseTimeoutError:
        logger.warning("Timed out loading user %s", user_id)
        raise
```
Use custom Exceptions specific for your application:
```
# Use `raise ... from e` to translate to a higher-level exception
# while preserving the original cause.
class ConfigError(Exception):
    pass

def load_port(config):
    try:
        return int(config["port"])
    except (KeyError, ValueError) as e:
        raise ConfigError("Invalid or missing `port` in config") from e
```
raise ... from e creates a new exception that says “this happened because of that,” so the traceback keeps the causal chain.


### Fail loudly

Never swallow unexpected bugs.

Good:
```python
try:
    user = repo.load(user_id)
except FileNotFoundError:
    return None
except PermissionError as e:
    raise UserLoadError(user_id) from e
```

Bad:
```python
try:
    user = repo.load(user_id)
except Exception:
    return None  # hides bugs, permissions, corruption
```

---

## Cleanup and resource safety

Use language features that make failure paths look as deliberate as success paths.

- Prefer context managers (`with`) for files, locks, DB sessions, and temporary state.
- Use `finally` only when a context manager is not available or you need multi-step cleanup.
- Async code follows the same rule: `async with`, `asyncio.timeout`, and cancellation-aware cleanup.

### Patterns

```python
from contextlib import suppress

# with handles cleanup automatically:
with open(path) as f:
    data = f.read()

lock.acquire()
try:
    update_cache()
finally:
    # finally always runs and ensured the lock is always released
    lock.release()

# supress is a tidy way to ignore errors
with suppress(FileNotFoundError):
    os.remove(tmp_path)
```

The suppress call above is equivalent:
```
try:
    os.remove(tmp_path)
except FileNotFoundError:
    pass
```

---

## Design exception types that match your API

Stable exception semantics are part of your interface.

### Custom hierarchy

Create a small base exception for your package and a few meaningful subclasses. Do not mirror every low-level failure 1:1 unless callers need that distinction.

```python
class PaymentError(Exception):
    pass

class CardDeclined(PaymentError):
    pass

class PaymentGatewayUnavailable(PaymentError):
    pass
```

### Translate at boundaries

Turn vendor- or driver-specific exceptions into domain exceptions near the boundary layer.

### Add context

Include identifiers, state, and actionable metadata in the exception message or attributes.

### Do not overload

Exceptions are not user messages, HTTP payloads, or retry policies by themselves.

---

## Logging, retries, and observability

Handle once at the layer that can add value.

### Log at boundaries

Avoid duplicate logging on every stack frame. Usually log where you are about to drop the exception, turn it into a response, or start a retry policy.

### Retry selectively

Retry transient failures like timeouts or 503s. Do not retry programmer bugs, bad inputs, or permanent policy failures.

### Keep traces

Include request IDs, dependency names, retry counts, and the original exception chain in logs or telemetry.

Anti-pattern: log + wrap + re-log at every level.

---

## Testing: Test your exception handling too!
Test the unhappy path on purpose
Error handling that is never tested is usually accidental.

### `pytest` pattern

```python
import pytest

def test_translates_timeout(mocker):
    mocker.patch('svc.client.fetch', side_effect=TimeoutError)

    with pytest.raises(ServiceUnavailable) as exc:
        get_profile('u1')

    assert 'u1' in str(exc.value)
    assert isinstance(exc.value.__cause__, TimeoutError)
```

- Inject failures with mocks, fakes, or fault-injection hooks.
- Assert on exception type first, message second, internals last.
- Test cleanup and partial-progress cases, not just the raised exception.
- For async code, test cancellation and timeout behavior explicitly.

Goal: predictable failure contracts.

---

## How Python differs from Go

Go treats most failures as explicit return values, not exceptions.

### Python

```python
# Python
def load_config(path):
    with open(path) as f:
        return json.load(f)
```

### Go

```go
// Go
func LoadConfig(path string) (Config, error) {
    f, err := os.Open(path)
    if err != nil {
        return Config{}, err
    }
    defer f.Close()
    ...
}
```

### Key differences

- **Control flow:** Python unwinds via exceptions. Go threads `error` through return values. This means Go requires lots of checking error return values and handling at every function call.
- **Cleanup:** Python uses `with` / `finally`. Go uses `defer`.
- **API shape:** Go APIs often expose many explicit error checks; Python APIs are usually cleaner at call sites but require disciplined boundaries.

---

## How Python differs from C++

C++ mixes exception-based designs with zero-exception codebases.

### C++ exceptions

```cpp
// C++ (exception style)
std::string read_file(const std::string& path) {
    std::ifstream f(path);
    if (!f) throw std::runtime_error("open failed");
    ...
}
```

### Modern alternative

```cpp
// C++ (no-exception style)
std::expected<Data, Error> parse(Input in);

// Python has no direct equivalent in stdlib;
// returning Result-like objects is a library choice.
```

### Key differences

- **Resource safety:** C++ leans on RAII (safe pointers): destructors clean up automatically during stack unwinding.
- **`noexcept` matters:** Throwing across code marked `noexcept` can terminate the program; exception guarantees are part of API design.
- **Culture differs:** Many C++ teams ban or limit exceptions for performance, ABI, or predictability reasons. Python does not have that norm.

---

## Quick comparison with other languages

Different ecosystems optimize for different trade-offs.

| Language | Primary model | Best at | Trade-off | Watch for |
|---|---|---|---|---|
| Python | exceptions | clean call sites | can hide control flow | broad `except` |
| Go | `error` returns | explicitness | verbose plumbing | ignored `err` |
| C++ | mixed: exceptions / `expected` | RAII + zero-cost abstractions | policy varies by codebase | exception guarantees |
| Java/C# | exceptions, often richer type systems | framework integration | checked exceptions in Java can become noisy | over-translation |
| Rust | `Result` + `?`, panic for bugs | compile-time visibility | more type plumbing | using panic where recoverable errors fit |

---

## Same task, different error model

Reading JSON config: identical problem, very different ergonomics.

### Python

```python
def load_config(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise ConfigError(path) from e
```

### Go

```go
func LoadConfig(path string) (Config, error) {
    f, err := os.Open(path)
    if err != nil { return Config{}, fmt.Errorf("%s: %w", path, err) }
    defer f.Close()
    ...
}
```

### C++

```cpp
Config load_config(const std::string& path) {
    std::ifstream f(path);
    if (!f) throw ConfigError(path);
    ...
}
```

- Python optimizes caller readability.
- Go optimizes explicitness.
- C++ optimizes by codebase policy.

---

## Common anti-patterns to remove in code review

These create brittle systems and terrible debugging sessions.

Bare except:
- Catches system-exiting exceptions too. Usually means “I do not know what failed.”
Silent fallback:
- Returning defaults for corrupted state or permission failures hides incidents.
String-matching errors:
- Rely on exception types and structured metadata, not fragile text parsing.
Translate everything:
- Repeated wrapping destroys signal and duplicates logs.

---

## Practical checklist

If your team follows these six rules, error handling gets dramatically better.

### Python checklist

1. Raise exceptions for real failure, not routine branching.
2. Catch only exceptions you can act on.
3. Use `raise from` when translating layers.
4. Prefer `with` / context managers for cleanup.
5. Log once, with context, at the right boundary.
6. Test failure paths intentionally.

### Cross-language intuition

- Go makes error flow explicit at every call site.
- C++ varies: exceptions, RAII, or `expected` depending on policy.
- Java/C# lean into exceptions more than Go, but often with more framework and type-system ceremony.
- Rust treats recoverable errors as values and unrecoverable bugs as panics.

**Best outcome:** failures are obvious, typed, and actionable.
