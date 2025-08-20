## Multi-threaded programming in Python

There are generally 3 ways to speed up a Python program:
1) Async: Do only one thing at a time, but use "co-routines" that can be paused and resumed to do other useful work instead of waiting for slow I/O (keyboard, disk, network, database, internet, etc)
2) Multi-Threading: Do multiple things at once, by simultaneously running several functions at the same time all in the same application accessing shared memory and variables.
3) Multi-Processing: Do multiple things at once, by simultaneously running several separate applications, each with their own Python interpreter, memory space, and variables. There are libraries to help the separate applications communicate with each other.

Until very recently, Multi-Threading was not as fast as it should have been in Python. Threads all had to wait for each other when any one thread accessed variables. Now starting with Python 3.13 and 3.14 there is a "free-threaded" version of Python can run threads at full speed. Still somewhat experimental and some libraries have not been updated to make full use of this yet.

## Multi-threading Patterns

*thread-per-task* create a thread to handle each separate type of work
Examples:
- Very common to have one thread do processing and another thread handle the user interface. This way the user interface doesn't "freeze" when there is processing going on.
- A web server that starts a new thread to handle each incoming request.

*thread-pool* have a fixed (or capped) pool of worker threads picking up tasks from a task queue. The main thread or a dispatcher thread puts tasks into the task queue. Also called 'producer/consumer'.
Examples:
- A web spider/crawler that has a dispatcher thread putting URLs into a task queue, and 5 worker threads spidering those URLs. Too few worker threads would spend time waiting to request the URLs, too many worker threads would cause contention for the network and the CPU. A fixed, but adjustable, number of worker threads would work best.
- A database server that has a dispatcher thread handling incoming client queries and putting them into a task queue for a fixed number of worker threads to process.



