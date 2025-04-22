## Classes
"""
- defining a class
- using init and self
- instantiating a class
- public private and protected attributes
- getter and setter methods
- property decorators
- inheritance, base class and derived class
- overriding methods
- super( )
- abstract base classes
- special methods: str( ) repr( ) add( ) sub( ) eq( ) lt( )
"""


class Car:

  def __init__(self, make, model, year):
    self.make = make
    self.model = model
    self.year = year

  def display_info(self):
    print(f"{self.year} {self.make} {self.model}")


# Creating an object of the Car class
my_car = Car("Toyota", "Corolla", 2022)
my_car.display_info()  # Output: 2022 Toyota Corolla


class Car:

  def __init__(self, make, model, year):
    self._make = make  # Note the underscore, indicating "protected" by convention
    self._model = model
    self._year = year

  @property
  def make(self):
    return self._make

  @make.setter
  def make(self, value):
    self._make = value


# Accessing and setting private attributes
my_car = Car("Toyota", "Corolla", 2022)
print(my_car.make)  # Toyota
my_car.make = "Honda"
print(my_car.make)  # Honda


class ElectricCar(Car):  # Inherits from Car

  def __init__(self, make, model, year, battery_size):
    super().__init__(make, model, year)
    self.battery_size = battery_size

  def display_info(self):
    super().display_info()
    print(f"Battery Size: {self.battery_size} kWh")


# Demonstrating method overriding
my_electric_car = ElectricCar("Tesla", "Model S", 2021, 75)
my_electric_car.display_info()  # Outputs Car info and Battery Size: 75 kWh


class GasCar(Car):

  def refuel(self):
    print("Refueling with gasoline.")


class ElectricCar(Car):

  def refuel(self):
    print("Charging the battery.")


def refuel_vehicle(car):
  car.refuel()


# Polymorphism in action
gas_car = GasCar("Ford", "Fusion", 2020)
electric_car = ElectricCar("Nissan", "Leaf", 2021)

refuel_vehicle(gas_car)  # Refueling with gasoline.
refuel_vehicle(electric_car)  # Charging the battery.

from abc import ABC, abstractmethod


class Vehicle(ABC):

  @abstractmethod
  def go(self):
    pass


class Car(Vehicle):

  def go(self):
    print("The car is going.")


# Attempting to instantiate Vehicle will raise an error
# vehicle = Vehicle()  # TypeError: Can't instantiate abstract class Vehicle with abstract methods go

# You can instantiate Car, which implements the go method
car = Car()
car.go()  # The car is going.


class Car:

  def __init__(self, make, model):
    self.make = make
    self.model = model

  def __str__(self):
    return f"{self.make} {self.model}"

  def __add__(self, other):
    return f"{self.model} and {other.model} combo"


# Using special methods
car1 = Car("Toyota", "Corolla")
car2 = Car("Honda", "Civic")
print(car1)  # Toyota Corolla
print(car1 + car2)  # Corolla and Civic combo
