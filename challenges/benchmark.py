# Library to run several different versions or algorithms side by side
# and benchmark which is faster
# Usage: import benchmark
#        # set up list of functions:
#        algorithms = [ { "method_fn":alg1, "title":"Simple brute force O(n^2)", "setup_fn":alg1_setup},
#                       { "method_fn":alg2, "title":"Use dict for faster access O(n)", "setup_fn":alg2_setup},
#                     ]
#        # run benchmarks:
#        benchmark.run( algorithms, REPEAT=1000)
#
# This will run each of the algorithms multiple times and calculate the elapsed time and the average individual time
# The setup function will be called once for each algorithm. It's result will be passed to the algorithm method as input
# benchmark.run() will output the results.
