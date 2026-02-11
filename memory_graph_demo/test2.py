# https://memory-graph.com/#breakpoints=8&continues=1&timestep=1.0&play
import memory_graph as mg

class My_Class:

    def __init__(self, x, y):
        self.x = x
        self.y = y

data = [ range(1, 2), (3, 4), {5, 6}, {7:'seven', 8:'eight'},  My_Class(9, 10) ]
mg.show(data)