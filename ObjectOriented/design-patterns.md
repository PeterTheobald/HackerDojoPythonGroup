## Object-Oriented Programming: Best Practices & Design Patterns

1. Core OOP Principles
- Encapsulation: Hide internal state; expose behavior via public methods
- Abstraction: Model real-world entities through simplified interfaces
- Inheritance: Reuse and extend behavior in a class hierarchy
- Polymorphism: Treat different types uniformly via a common interface
#### Encapsulation
``` python
class BankAccount:
    def __init__(self):
        self.__balance = 0.0    # private attribute
    def deposit(self, amt):
        if amt > 0:
            self.__balance += amt
    def get_balance(self):
        return self.__balance
```
#### Abstraction

**Abstract base class for shapes**
``` python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        raise NotImplementedError("subclasses of Shape must implement area()") # better than using "pass"
```

#### Inheritance
``` python
class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h
```
#### Polymorphism
``` python
class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.1416 * self.r**2

shapes = [Rectangle(3,4), Circle(5)]
for s in shapes:
    print(s.area())    # works for any Shape
```
**Python doesn't explicitly have "interfaces", but uses Duck Typing. One way to explicitly define an interface is by using an Abstract Base Class. Another way is by using typing Protocol (not shown here)**
``` python
from abc import ABC, abstractmethod

class Iterator(ABC):
    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self):
        raise NotImplementedError("Subclasses must implement __next__") # redundant, can just use "pass"

class MyRange(Iterator):
    def __init__(self, start: int, end: int):
        self.current = start
        self.end = end

    def __next__(self) -> int:
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

# Example usage:
for i in MyRange(1, 5):
    print(i)
# Output: 1 2 3 4
```
2. Best Practices
- Single Responsibility: One class: one reason to change
- Open/Closed: Open to extension, closed to modification
- Dependency Inversion: Depend on abstractions, not concretions
- Favor Composition over Inheritance: Assemble behavior at runtime
- Use Interfaces & Abstract Classes: Define contracts, minimize coupling
- Consistent Naming & Formatting: Improves readability and navigation
- Write Small, Cohesive Methods: Easier to test and maintain
- Automated Testing & Code Reviews: Catch design flaws early
#### Single Responsibility
``` python
class MessageFormatter:
    def format(self, msg):
        return f"[{msg.upper()}]"

class FileWriter:
    def write(self, path, msg):
        with open(path, 'a') as f:
            f.write(msg + '\n')
```
#### Open/Closed
``` python
class Discount(ABC):
    @abstractmethod
    def apply(self, price): pass

class SeasonalDiscount(Discount):
    def apply(self, price):
        return price * 0.9
# add new discounts via new subclasses
```
#### Dependency Inversion
``` python
class PaymentGateway(ABC):
    @abstractmethod
    def pay(self, amt): pass

class StripeGateway(PaymentGateway):
    def pay(self, amt): print(f"Stripe: {amt}")

class OrderProcessor:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway
    def process(self, amt):
        self.gateway.pay(amt)
```
#### Composition over Inheritance
``` python
class Printer:
    def print(self, text): print(text)

class Report:
    def __init__(self, printer: Printer):
        self.printer = printer
    def generate(self):
        self.printer.print("Report data")
```
3. SOLID Principles
- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion
#### Liskov Substitution
``` python
def print_area(shape: Shape):
    print(shape.area())  # any Shape works
```
#### Interface Segregation
``` python
class Scanner(ABC):
    @abstractmethod
    def scan(self): pass

class Printer(ABC):
    @abstractmethod
    def print(self): pass

class MFP(Scanner, Printer):
    def scan(self): ...
    def print(self): ...
```
4. Common Design Patterns
- Creational: Factory, Singleton, Builder, Abstract Factory, Prototype
- Structural: Adapter, Decorator, Facade, Proxy, Composite
- Behavioral: Observer, Strategy, Command, Iterator, State, Template Method, Mediator
- Intent & Use-Case for each pattern
- Pros & Cons and consequences of adoption
- Guidance on when to refactor toward a pattern
#### Factory
``` python
class ShapeFactory:
    @staticmethod
    def create(type_, *args):
        return {'rect': Rectangle, 'circle': Circle}[type_](*args)
```
#### Singleton
``` python
class SingletonMeta(type):
    _inst = None
    def __call__(cls, *a, **k):
        if not cls._inst:
            cls._inst = super().__call__(*a, **k)
        return cls._inst

class Config(metaclass=SingletonMeta):
    pass
```
#### Decorator
``` python
class Notifier:
    def send(self, msg): print("Base:", msg)

class SMSDecorator(Notifier):
    def __init__(self, wrap):
        self.wrap = wrap
    def send(self, msg):
        self.wrap.send(msg)
        print("SMS:", msg)
```
#### Strategy
``` python
class Strategy(ABC):
    @abstractmethod
    def execute(self): pass

class FastStrategy(Strategy):
    def execute(self): print("Fast")

class Context:
    def __init__(self, strat: Strategy):
        self.strat = strat
    def run(self):
        self.strat.execute()

Context(FastStrategy()).run()
```

5. Pattern Selection & Integration
- Analyze requirements → choose simplest pattern that fits
- Combine patterns where appropriate (e.g., Factory + Singleton)
- Refactor incrementally; verify via unit tests
#### Compose patterns:
``` python
strat = {'fast': FastStrategy, 'slow': SlowStrategy}['fast']()
Context(strat).run()
```
6. Refactoring & Anti-Patterns
- Recognize code smells (e.g., God object, shotgun surgery, Feature Envy)
- Refactor toward patterns to improve structure
- Continuously review and adapt refactor as requirements evolve
#### Code Smell: large class doing too much
``` python
# before: UserService handles parsing, validating, saving
class UserService: ...
# after:
class UserParser: ...
class UserValidator: ...
class UserRepository: ...
```
<hr>
The famous "Gang of Four" book that started it:
“Design Patterns” (Gamma et al.),





