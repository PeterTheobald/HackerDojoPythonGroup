from typing import Protocol

class Quacker(Protocol):
  def make_it_quack(self):
    ...

class Duck():
    def make_it_quack(self):
        return "The duck is quacking!"

class Person():
    def make_it_quack(self):
        return "The person is imitating a duck quacking!"

def make_it_quack(animal: Quacker) -> str:
    return animal.make_it_quack()

print(make_it_quack(Duck()))

print(make_it_quack(Person()))

