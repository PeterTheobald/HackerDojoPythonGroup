def f1(a):
  return 1 / a


f2 = lambda a: 'even' if a%2==0 else 'odd'


my_function( 'even' if a%2==0 else 'odd')

def get_key(x: int) -> int:
  return x[1]


#sorted(my_list, key=get_key)

import functools

# print(functools.reduce(lambda acc, val: acc + val, [2, 3, 4, 6, 7, 8]))

print(  [x * 2 for x in [2, 3, 6, 8]]  )


# IIFE
# immediately invoked function expression
# wikipedia.org/wiki/Immediately_invoked_function_expression

# https://peps.python.org/pep-0008/



def my_f(a):
  return a+1

f2=my_f

def high_order_f( user_fn, val):
  user_fn(val)
