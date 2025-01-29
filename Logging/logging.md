# Python logging

## Simplest: print logging
```
    print(value)

## Logging module

1. Can standardize logged information 
2. Can filter output by severity: DEBUG INFO WARNING ERROR CRITICAL
3. Can scale multiple processes and servers into consolidated log files
4. Can search/filter consolidated log files

## Basic usage
```
import logging

# By default, logging logs messages with a severity level of WARNING or above.
logging.warning("This is a warning")
logging.info("This won't show up by default")
logging.error("This is an error")
```

When you run your program, by default WARNING ERROR CRITICAL will print on screen (stdout)
You can use a flag to change what shows on screen
You can leave verbose debugging info in the code with logging.debug() and just use flags or configs to turn it on and off.

## custom config
```
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Show all messages from DEBUG and above
    filename='sampleprog.log'
    format="%(asctime)s - %(name)s - %(levelname)s - %(lineno)d %(message)s"
)

logging.debug("This is a debug-level message.")
logging.info("This is an info-level message.")
logging.warning("This is a warning-level message.")
```

## command line arg to set log level
Use a command line arg to turn on and off debug level logging. You can leave the debug info in the code without removing it or commenting it out.

```
import argparse
import logging
import sys

def main():
    parser = argparse.ArgumentParser(description="My Application")
    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level"
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)
    logging.debug("This is a DEBUG message.")
    logging.info("This is an INFO message.")
    logging.warning("This is a WARNING message.")
    logging.error("This is an ERROR message.")
    logging.critical("This is a CRITICAL message.")

if __name__ == "__main__":
    sys.exit(main())
```
## Standard field in the formatter

Placeholder	Description
%(name)s	Name of the logger (logger.name).
%(levelno)s	Numeric log level for the message (e.g., 10 for DEBUG, 20 for INFO, 30 for WARNING, etc.).
%(levelname)s	Text log level (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").
%(pathname)s	Full path of the source file where the logging call was made.
%(filename)s	Filename portion of the path of the source file.
%(module)s	Module name of the caller (which is typically filename without the .py extension).
%(lineno)d	Line number in the source file where the logging call was made.
%(funcName)s	Name of the function or method from which the logging call originated.
%(created)f	Time (as a floating-point number) when the LogRecord was created, in seconds since the epoch (time.time()).
%(asctime)s	Human-readable time string when the LogRecord was created (by default: YYYY-MM-DD HH:MM:SS,mmm).
%(msecs)d	Millisecond portion of the timestamp in asctime.
%(relativeCreated)d	Time in milliseconds since the logging module was loaded. Useful for seeing how long your program has been running.
%(thread)d	Thread ID (if available).
%(threadName)s	Thread name (if available).
%(process)d	Process ID (if available).
%(message)s	The final text message after applying any msg % args manipulations.

## Extra fields in the formatter
You can define custom fields to add to the log format
```
import logging

# Configure the root logger to handle DEBUG messages
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(user)s@%(ip)s: %(message)s"
)

# Get a logger
logger = logging.getLogger(__name__)

# Log some messages, including extra fields
logger.info("User login successful", extra={"user": "Alice", "ip": "192.168.0.1"})
logger.info("User logout", extra={"user": "Bob", "ip": "192.168.0.2"})
```


## Multiple loggers
You may need to send different levels of logging to different destinations to screen, file etc
You can create a logger for each configuration
```
import logging

# Create a custom logger
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)

# Create console handler with a specific log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create file handler with a higher log level
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.WARNING)

# Create a formatter for these handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Generate logs at different levels
logger.debug("Debug message goes to console.")
logger.info("Info message goes to console.")
logger.warning("Warning also goes to the file app.log.")
logger.error("Error message goes to console and file.")
logger.critical("Critical issue goes to console and file.")
```

## Log rotation
When log files get too big, you have to open a new log file, keep some and delete old ones
This is often done with a script being called once a day or more frequently

But logging can do this for you automatically

Rotate by size:

```
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("rotating_example")
logger.setLevel(logging.INFO)

# Rotate file after it reaches 1MB, and keep up to 3 backups
handler = RotatingFileHandler("app_rotating.log", maxBytes=1_000_000, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

for i in range(10000):
    logger.info(f"This is log entry number {i}")

```

Rotate by time:

```
import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger("timed_example")
logger.setLevel(logging.INFO)

# Create a new log file every day (midnight) and keep 7 backups
handler = TimedRotatingFileHandler("app_timed.log", when="midnight", backupCount=7)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

logger.info("This log entry will be automatically rotated every midnight.")
```

## Modules with different logging configs

main.py
```
import logging
import some_module

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logging.info("Main function started")
    some_module.run_task()

if __name__ == "__main__":
    main()
```

and the module:
some_module.py
```
import logging

# Create or get a logger specific to this module
logger = logging.getLogger(__name__)

def run_task():
    logger.info("Running task in some_module")
    # ...
```

## Sending to network log server

Standard Linux SYSLOG server:
```
import logging
from logging.handlers import SysLogHandler

# Create a logger
logger = logging.getLogger("my_app")
logger.setLevel(logging.INFO)

# Create a SysLogHandler pointing to a syslog server (IP/hostname & port)
# Default port is 514 for UDP syslog; use TCP if your server supports it.
syslog_handler = SysLogHandler(address=("your-syslog-server.com", 514))
syslog_handler.setLevel(logging.INFO)

# Format the syslog message
# A typical syslog format might include a program name and the log level
formatter = logging.Formatter("%(name)s: %(levelname)s %(message)s")
syslog_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(syslog_handler)

# Send a test message
logger.info("This is a test log via SysLogHandler.")
```

Or better more reliable, use TCP instead of UDP but only if your server is configured to accept it:
```
SysLogHandler(address=("your-syslog-server.com", 514), socktype=socket.SOCK_STREAM)
```

Lower level send logs to a custom log server on any network TCP socket port or UDP datagram port

### send via TCP Socket:
```
import logging
import socket
from logging.handlers import SocketHandler

logger = logging.getLogger("my_tcp_logger")
logger.setLevel(logging.DEBUG)

# Replace "server_host" and "server_port" with your actual TCP server address
socket_handler = SocketHandler("server_host", server_port)
socket_handler.setLevel(logging.DEBUG)

logger.addHandler(socket_handler)

logger.info("Sending log to a custom TCP log server.")
```

### send via UDP datagrams:
```
import logging
from logging.handlers import DatagramHandler

logger = logging.getLogger("my_udp_logger")
logger.setLevel(logging.INFO)

udp_handler = DatagramHandler("server_host", server_port)  # UDP-based
udp_handler.setLevel(logging.INFO)

logger.addHandler(udp_handler)

logger.info("Sending log to a custom UDP log server.")
```

### send via HTTP REST API:
```
import logging
from logging.handlers import HTTPHandler

logger = logging.getLogger("my_http_logger")
logger.setLevel(logging.INFO)

# Replace with your log ingestion endpoint
http_handler = HTTPHandler(
    host="api.loggingservice.com",  # "host:port" or just "host"
    url="/logs",                   # Path to the endpoint
    method="POST"                  # "GET" or "POST"
)
http_handler.setLevel(logging.INFO)

logger.addHandler(http_handler)

logger.info("Sending log via HTTPHandler.")
```

## High volume logging
Logging can be a lot of I/O. If you are concerned with how much traffic your logs generate, especially over the network, you can log to a buffered MEMORY handler that queues up logs and then writes or sends them all at once in large batches. This is more efficient than many smaller writes or sends.

```
import logging
import socket
from logging.handlers import MemoryHandler, SocketHandler

# Suppose you have a remote log server at "log.mycompany.com" on port 9000
socket_handler = SocketHandler("log.mycompany.com", 9000)
socket_handler.setLevel(logging.DEBUG)

# Wrap the socket_handler with MemoryHandler
memory_handler = MemoryHandler(
    capacity=1000,
    flushLevel=logging.ERROR,
    target=socket_handler,
)

logger = logging.getLogger("netBufferedLogger")
logger.setLevel(logging.DEBUG)
logger.addHandler(memory_handler)

for i in range(5000):
    logger.debug(f"Network debug event {i}")

# Ensure everything is sent before the script terminates
memory_handler.flush()
```

### Considerations for High-Volume Logging
- Memory Usage: Storing a large number of log records in memory can consume a lot of RAM. Choose capacity wisely.
- Performance: In general, buffering improves performance by reducing I/O calls. However, if you set flushLevel too low (e.g., logging.INFO), you could end up flushing too often.
- Graceful Shutdown: If your application might terminate unexpectedly, ensure that logs are flushed in critical situations (e.g., try/finally or at the end of the script).
- QueueHandler: If you need asynchronous logging, consider the QueueHandler (and QueueListener) approach, which can offload log handling to a separate thread or process.


## advanced

- Be aware of security. Some of these send logs over the network unencrypted.
- Loki is a well known central log server with a user interface for searching and filtering logs. It's made by Grafana Labs which has other "observability" tools. It can scale horizontally to multiple servers. It has a query language. It works well with Grafana to make dashboards and charts and graphs based on the data. It can even work without sending logs over the network by running the "Promtail" agent which watches the end of your log file and sending new logs to the server. It can store logs locally, across a cluster of Loki's or in cloud storage like S3.

