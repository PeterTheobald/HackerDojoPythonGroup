def add(a: Union[float, int], b: Union[float, int]) -> float:
    return float(a+b)

a=add(5.4,1.1)
print(a, type(a))
a=add(5,1)
print(a, type(a))
a=add("5","1")
print(a, type(a))

