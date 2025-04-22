

class Vehicle:
  @abstractmethod
  def accelerate(self):
    pass


class Car(Vehicle):
  def __init__(self, make, model):
    self._make = make
    self._model = model
  def display(self):
    """display shows the contents of the car"""
    print(f"I am a {self._make} {self._model}")
  @property
  def make(self):
    return self._make
    
  @make.setter
  def make(self, newval):
    self._make = newval
  def __str__(self):
    return f"Car {self._make} {self._model}"
  def __repr__(self):
    return f"{self._make},{self._model}"
  def __add__(self, othercar):
    self._make = self._make+","+othercar.make
    return self._make

class sportscar(Car):
  def display(self):
    print("ZOOM ZOOM ", super.__str__(self))


  
c=Car('toyota', 'sienna')
d=Car('ford', 'mustang')
c.display()

e=sportscar('ferrari', 'the-red-one')
e.display()

