class Car():
    def __init__(self, make, model, year='2025'):
        self.make=make
        self.model=model
        self.year=year
        self.mileage=0

    def drive(self, miles):
        self.mileage += miles
        print(f'Just drove {miles} in my {self.make} {self.model}')

class ElectricCar( Car):
    def __init__(self, make, model, year=2025):
        super().__init__(make, model, year)
        self.battery=300
    def drive(self, miles):
        super().drive(miles)
        self.battery -= miles
        if self.battery < 0:
            print('You ran out of battery')
            self.battery=0
    def __str__(self):
        return f'a {self.year} {self.make} {self.model}'
    def __repr__(self):
        return f'a {self.year} {self.make} {self.model}'
