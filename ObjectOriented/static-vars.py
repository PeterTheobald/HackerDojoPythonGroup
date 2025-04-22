# Example of Class shared static variables (atttributes)
# One value that all object instances of the Class will share

class MyClass:
  static_string = "default"

  def change1(self, val):
    MyClass.static_string = val
    # YES! STATIC VALUE SHARED BY ALL OBJECT IN CLASS

  def change2(self, val):
    self.static_string = val
    # NO! Dangerous we just created an instance variable
    # that can be confused with MyClass.static_string

# To avoid confusion, always refer to MyClass.static_string

x = MyClass()
print(f"class var: {MyClass.static_string}, instance var: {x.static_string}")

x.change1("new shared static value")
print(f"class var: {MyClass.static_string}, instance var: {x.static_string}")

x.change2("new instance variable with same name, confusing")
print(f"class var: {MyClass.static_string}, instance var: {x.static_string}")

""" Output:
class var: default, instance var: default
class var: new shared static value, instance var: new shared static value
class var: new shared static value, instance var: new instance variable with same name, confusing
"""
