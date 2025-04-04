import tracemalloc

tracemalloc.start()

# Code suspected of leaking
leaky_list = []
for i in range(10000):
    leaky_list.append(object())

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[ Top 5 memory allocations ]")
for stat in top_stats[:5]:
    print(stat)

