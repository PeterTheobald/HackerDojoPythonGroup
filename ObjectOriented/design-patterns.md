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

#### Misc descriptions of concepts:

#### Encapsulation
Encapsulation is the practice of bundling an object’s data (its state) and the methods that operate on that data within a single unit, the class, and restricting direct access to some of the object’s components. By exposing only a controlled interface (public methods) and keeping internal details hidden (private attributes), encapsulation enforces invariants and prevents external code from putting an object into an invalid state. This leads to more reliable, maintainable code, since implementation details can change without affecting clients that rely on the public interface.

#### Abstraction
Abstraction involves presenting only the essential features of an object to the outside world while hiding the complex underlying implementation. By defining clear interfaces or abstract classes that describe what operations are available, abstraction reduces cognitive load and allows developers to think at a higher level, focusing on what needs to be done rather than how. As requirements evolve, implementations can be swapped or optimized without impacting code that depends solely on the abstract interface.

#### Inheritance
Inheritance enables a new class (subclass) to reuse and extend the behavior of an existing class (superclass), promoting code reuse and logical organization of related types. It lets subclasses inherit attributes and methods, overriding or augmenting them to provide specialized behavior. While powerful, inheritance must be used judiciously—overly deep hierarchies can lead to fragile designs—so it’s often balanced with composition to maintain flexibility.

#### Polymorphism
Polymorphism allows objects of different classes to be treated uniformly based on a shared interface, letting the same operation name invoke different behaviors at runtime. Whether achieved through method overriding (subclass substitutability) or duck typing in dynamic languages, polymorphism decouples code from specific implementations. This flexibility makes it easier to extend systems with new types and reduces conditional logic that branches on type.

#### Single Responsibility
The Single Responsibility Principle mandates that a class or module should have one, and only one, reason to change—i.e., it should encapsulate exactly one piece of functionality or business concern. By keeping responsibilities focused and isolated, classes become easier to understand, modify, test, and reuse. When a class grows to handle multiple concerns, it often becomes a maintenance burden and a hotspot for bugs.

#### Open/Closed
The Open/Closed Principle states that software entities (classes, modules, functions) should be open for extension but closed for modification. In practice, this means designing systems so new behavior can be added—via subclassing, composition, or plugins—without altering existing, tested code. Adhering to Open/Closed reduces regression risk and makes evolving requirements more manageable.

#### Dependency Inversion
Dependency Inversion prescribes that high-level modules should not depend on low-level modules; both should depend on abstractions (e.g., interfaces or abstract classes). Furthermore, abstractions should not depend on details; details should depend on abstractions. This decoupling makes components more interchangeable and testable, since implementations can be swapped without changing high-level logic.

#### Favor Composition over Inheritance
Favoring composition over inheritance means assembling objects with varied functionalities at runtime by including instances of other classes, rather than inheriting behavior through class hierarchies. Composition offers greater flexibility: behaviors can be mixed and matched or replaced dynamically, and it avoids some of the pitfalls of deep inheritance chains such as tight coupling and fragile base classes. It encourages building small, focused components that collaborate through well-defined interfaces.

#### Use Interfaces & Abstract Classes
Defining interfaces or abstract base classes creates explicit contracts that implementations must fulfill, decoupling clients from concrete classes. Interfaces specify what operations are available without prescribing how they must be carried out, enabling multiple implementations and facilitating testing with mocks or stubs. Abstract classes can provide shared scaffolding while still enforcing that subclasses supply specific behaviors.

#### Consistent Naming & Formatting
Consistent naming and formatting across a codebase enhance readability, reduce cognitive friction, and help maintain a uniform style that teams can easily follow. Using clear, descriptive names for classes, methods, and variables, along with adhering to agreed-upon indentation, brace placement, and spacing conventions, makes it simpler for new developers to onboard and for reviewers to spot anomalies. Style guides and automated linters help enforce this consistency.

#### Write Small, Cohesive Methods
Methods should be short—ideally focused on a single task—and cohesive, meaning every line in the method contributes directly to its purpose. Small methods are easier to read, test, debug, and maintain; they encourage reuse and reduce duplication. When a method exceeds about 20–30 lines or performs multiple logical steps, it’s often a sign that it should be refactored into smaller helper methods.

#### Automated Testing & Code Reviews
Automated testing—unit, integration, and end-to-end—provides a safety net that catches regressions and verifies behavior as the code evolves. Coupling tests with continuous integration ensures that changes don’t break existing functionality. Code reviews bring human insight to design and style, enabling collective code ownership, improving quality, and sharing knowledge across the team.

#### Liskov Substitution
The Liskov Substitution Principle requires that objects of a superclass can be replaced with objects of a subclass without altering the correctness of the program. Subclasses must honor the promises (contracts) made by their base classes—preserving preconditions, postconditions, and invariants—so that clients relying on the base type remain unaffected. Violations lead to surprising behavior and brittle hierarchies.

#### Interface Segregation
Interface Segregation advocates for many fine-grained interfaces rather than a few large, “fat” ones, ensuring that clients depend only on the methods they actually use. This prevents classes from being forced to implement irrelevant operations and keeps abstractions focused. Smaller interfaces facilitate easier mocking in tests and reduce coupling between components.

#### Factory
The Factory pattern centralizes object creation logic in a dedicated component, often encapsulating conditional logic or configuration details. Clients request objects by type or parameters, and the factory returns the appropriate concrete instance. This decouples client code from concrete classes and simplifies changes to instantiation processes.

#### Singleton
The Singleton pattern ensures that a class has only one instance and provides a global access point to it. While useful for managing shared resources or configurations, singletons must be used sparingly due to hidden dependencies, challenges in testing, and potential for introducing global state that complicates concurrency and reuse.

#### Builder
The Builder pattern separates the construction of a complex object from its representation, allowing the same construction process to create different representations. A builder object offers a fluent interface or step-by-step methods to configure parts of the product, culminating in a final build operation. It’s ideal for objects with many optional parameters.

#### Abstract Factory
An Abstract Factory defines an interface for creating families of related or dependent objects without specifying their concrete classes. Clients interact with the factory interface to obtain product variants that are guaranteed to work together, promoting consistency across object families and simplifying swapping entire product sets.

#### Prototype
The Prototype pattern creates new objects by cloning an existing “prototype” instance, bypassing costly constructors or complex setup. Objects support a clone operation that returns a deep or shallow copy, enabling rapid duplication and dynamic specification of object types at runtime.

#### Adapter
The Adapter pattern converts the interface of one class into another interface clients expect, enabling classes with incompatible interfaces to work together. By wrapping the adaptee in an adapter with the desired interface, existing functionality can be reused without touching original code.

#### Decorator
The Decorator pattern attaches additional responsibilities to objects dynamically by wrapping them in decorator objects that implement the same interface. Each decorator adds behavior before or after delegating to the wrapped object, supporting flexible, runtime composition of features without subclassing.

#### Facade
The Facade pattern provides a simplified, high-level interface to a complex subsystem, hiding its internals and reducing dependencies. Clients interact with the facade instead of many subsystem classes, making usage easier and decoupling client code from detailed subsystem changes.

#### Proxy
The Proxy pattern uses a surrogate or placeholder object to control access to a real subject, adding layers such as lazy loading, access control, or logging. The proxy implements the same interface as the real object, transparently interposing itself in client requests.

#### Composite
The Composite pattern composes objects into tree structures to represent part-whole hierarchies, allowing clients to treat individual objects and compositions uniformly via a common interface. Operations applied to a composite automatically propagate to its child components.

#### Observer
The Observer pattern defines a one-to-many dependency: when one object’s state changes, all its dependents (observers) are notified and updated automatically. This decouples the subject from its observers, supporting event-driven architectures and publish-subscribe mechanisms.

#### Strategy
The Strategy pattern defines a family of interchangeable algorithms encapsulated in separate classes, letting clients choose an algorithm at runtime. By decoupling the algorithm from the context, strategies can be added or swapped independently of client code.

#### Command
The Command pattern encapsulates a request as an object, parameterizing clients with operations, queuing or logging requests, and supporting undoable actions. Each command object exposes an execute method (and often undo), decoupling the invoker from the receiver.

#### Iterator
The Iterator pattern provides a uniform way to traverse the elements of an aggregate object without exposing its underlying representation. By offering a separate iterator object with methods like hasNext and next, collections can be iterated flexibly and consistently.

#### State
The State pattern allows an object to alter its behavior when its internal state changes by delegating state-specific behavior to separate state objects. Clients interact with the context uniformly, while state objects implement variant behaviors and transitions.

#### Template Method
The Template Method pattern defines the skeleton of an algorithm in a base class method, deferring some steps to subclasses. Subclasses override specific steps without changing the overall algorithm structure, promoting code reuse and consistent workflows.

#### Mediator
The Mediator pattern centralizes complex communications and control logic between related objects in a single mediator object, reducing direct dependencies among them. Components communicate through the mediator, which orchestrates interactions and enforces loose coupling.

#### Recognize Code Smells
Code smells are surface indications of deeper problems; for example, a God Object that does too much or Shotgun Surgery where a small change requires touching many classes. Being able to spot these smells early—alongside metrics like high cyclomatic complexity or tight coupling—guides refactoring toward cleaner, more maintainable designs.





