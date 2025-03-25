## Using Python to Make Command Line Tools for Text File Processing

1. Make an executable script
2. Parse command line arguments
3. File read loop, reading and writing, encoding, error handling
4. Parsing: string manipulation, split, regex, etc
5. Types of files: log files, csv files, json files



## Make an executable script

The simple way:
  ```bash
  $ cat my_tool.py
  print('I am now running.')
  
  $ python my_tool.py ( or uv run my_tool.py)
  I am now running.
  ```

Use uv to make it more like a command line tool:
```bash
$ cat my_tool.py
#!/usr/bin/env -S uv run
print('I am now running.')

$ chmod u+x my_tool.py
$ cp my_tool.py ~/.local/bin
$ my_tool.py
I am now running.
```

gives you command line completion:
```bash
$ my_<tab>
$ my_tool.py
```
  
## Handle command line arguments

- sys.argv (raw list),
- argparse (standard, verbose),
- **click** (powerful),
- **typer** (uses type annotations),
- fire (easy),
- arguably (uses docstrings)

```
$ uv add --script click_demo.py click
```

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click",
# ]
# ///
import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")

if __name__ == '__main__':
    hello()
```

```bash
$ uv add --script click_demo.py click
$ chmod u+x click_demo.py
$ ./click_demo.py --count=3
Your name: Peter
Hello Peter!
Hello Peter!
Hello Peter!

$ ./click_demo.py --help
Usage: hello.py [OPTIONS]

  Simple program that greets NAME for a total of COUNT times.

Options:
  --count INTEGER  Number of greetings.
  --name TEXT      The person to greet.
  --help           Show this message and exit.
```

### Reading and writing files

Use `with` to get automatic close and cleanup
```python
with open('filename', 'r') as infile:
	# do stuff
```

```python
with open('filename', 'r') as infile:
	with open('outfile', 'w') as outfile:
		# do stuff
```

Read the entire file into one variable (slurping): (big memory usage)
```python
with open('example.txt', 'r') as file:
    data = file.read()
print(data)
```

Read the file one line at a time:
```python
with open('example.txt', 'r') as file:
    for line in file:
        print(line)
```

Cleaning newlines ("chomping" in Perl slang):
```python
with open('example.txt', 'r') as file:
    for line in file:
        clean_line = line.rstrip('\n')
        print(clean_line)
```

Specifying encoding: UTF-8, ASCII, Latin-1 etc.
```python
with open('example.txt', 'r', encoding='utf-8') as file:
    for line in file:
        clean_line = line.rstrip('\n')
        print(clean_line)
```

You never know what you might find in an input file. Prevent it from crashing your script with `errors=ignore` or `errors=replace`
```python
with open('illegal.txt', 'r', encoding='utf-8') as file:
    data_replace = file.read()
print(data_replace)
```

```python
with open('illegal.txt', 'r', encoding='utf-8', errors='replace') as file:
    data_replace = file.read()
print("Data read with errors replaced with � symbols:")
print(data_replace)
```

Writing a file:
```python
# Copy a file skipping blank lines
input_filename = 'example.txt'
output_filename = 'output.txt'

with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename, 'w', encoding='utf-8') as outfile:
    for line in infile:
        if line.strip():  # Only write non-blank lines
            outfile.write(line)
```

Error handling:
```python
# Example 1: Checking for file existence before reading
import os

filename = 'example.txt'
if os.path.exists(filename):
	# race condition right here...
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read()
    print(data)
else:
    print(f"File '{filename}' does not exist.")
```

```python
# Example 2: Using try/except to handle file reading errors
filename = 'example.txt'
try:
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read()
    print(data)
except FileNotFoundError:
    print(f"File '{filename}' not found.")
except Exception as e:
    print("An error occurred:", e)
```
Note: leave off the `except Exception as e` to allow any other errors to be (not) handled as normal

## Parsing string handling, split, regex, 

Use `string.split(delimeter)` to break up string into list
```python
with open('example.txt', 'r', encoding='utf-8') as infile:
    for line in infile:
        # Split the line into a list of words using whitespace as the delimiter
        words = line.split()
        print(words)
```

Use regex to break up string in more complex ways
```python
import re

with open('example.txt', 'r', encoding='utf-8') as infile:
    for line in infile:
        # Use regex to find all word characters
        words = re.findall(r'\w+', line)
        print(words)
```

or to "capture" specific things from the file:
```python
import re

# Regex pattern to match phone numbers in common formats (e.g., 123-456-7890, (123) 456-7890)
phone_regex = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')

with open('example.txt', 'r', encoding='utf-8') as infile:
    content = infile.read()
    phone_numbers = re.findall(phone_regex, content)
    for number in phone_numbers:
        print(number)
```

Regex functions:
- `re.search()`: Scans through a string and returns the first match.
- `re.match()`: Checks for a match only at the beginning of the string.split
- `re.findall()`: Returns a list of all non-overlapping matches in the string.split
- `re.sub()`: Replaces parts of a string that match a pattern with a replacement string.

## Log files, CSV files, JSON files

Webserver common log file format(s):
- Apache's Common Log Format (CLF), Apache's Combined Log Format, the W3C Extended Log File Format (ELF), and syslog formats (RFC 5424)

```
192.168.1.100 - - [25/Mar/2025:10:15:30 -0400] "GET / HTTP/1.1" 200 5120
192.168.1.101 - - [25/Mar/2025:10:15:32 -0400] "GET /images/logo.png HTTP/1.1" 200 1024
192.168.1.102 - - [25/Mar/2025:10:15:35 -0400] "GET /css/styles.css HTTP/1.1" 200 2048
192.168.1.103 - - [25/Mar/2025:10:15:37 -0400] "GET /js/app.js HTTP/1.1" 200 3072
192.168.1.104 - - [25/Mar/2025:10:15:40 -0400] "POST /api/data HTTP/1.1" 201 512
192.168.1.105 - - [25/Mar/2025:10:15:45 -0400] "GET /about HTTP/1.1" 200 1024
```

Use Regex tool like https://regex101.com/ to troubleshoot regex patterns

```python
import re

log_pattern = re.compile(
    r'(?P<ip>\S+) - - \[(?P<time>[^\]]+)\] "(?P<request>[^"]+)" (?P<status>\d{3}) (?P<bytes>\d+)'
)

with open("webserver.log", "r") as logfile:
    for line in logfile:
        match = log_pattern.match(line)
        if match:
            entry = match.groupdict()
            parts = entry['request'].split()
            if len(parts) == 3:
                entry['method'], entry['url'], entry['protocol'] = parts
            print(entry)

```

CSV files:

```csv
id,name,age,city
1,John Doe,28,New York
2,Jane Smith,32,Los Angeles
3,Bob Johnson,45,Chicago
4,Alice Williams,29,Houston
5,Michael Brown,33,Phoenix
6,Linda Davis,27,Philadelphia
7,Robert Miller,40,San Antonio
8,"Patricia Wilson, 3rd",36,San Diego
9,David Moore,22,Dallas
```

```python
import csv

with open('sample.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)
```

```python
import pandas as pd

df = pd.read_csv("sample.csv")
print(df)
```

JSON files:

```python
[
  {"id": 1, "name": "John Doe", "age": 28, "city": "New York"},
  {"id": 2, "name": "Jane Smith", "age": 32, "city": "Los Angeles"},
  {"id": 3, "name": "Bob Johnson", "age": 45, "city": "Chicago"},
  {"id": 4, "name": "Alice Williams", "age": 29, "city": "Houston"},
  {"id": 5, "name": "Michael Brown", "age": 33, "city": "Phoenix"},
  {"id": 6, "name": "Linda Davis", "age": 27, "city": "Philadelphia"},
]
```

```python
import json

with open("sample.json", "r") as file:
    data = json.load(file)
    print(data)
```

```python
import pandas as pd

df = pd.read_json("sample.json")
print(df)
```

