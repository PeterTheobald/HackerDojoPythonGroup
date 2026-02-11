# https://memory-graph.com/#breakpoints=8&continues=1&timestep=1.0&play
import memory_graph as mg
# Note: sudo apt install graphviz

# create the lists 'a' and 'b'
a = [4, 3, 2]
b = a
c = a.copy() # c is a copy of a, not the same list
b.append(1) # changing 'b' changes 'a'

# print the 'a' and 'b' list
print('a:', a)
print('b:', b)

# check if 'a' and 'b' share the list
print('ids:', id(a), id(b))
print('identical?:', a is b)

# show all local variables in a graph
# Note: memory_graph defaults to PDF format
# To get PNG, set format in environment or use show() default behavior
mg.show(locals())
print("Graph saved to memory_graph.pdf (will auto-open)")

