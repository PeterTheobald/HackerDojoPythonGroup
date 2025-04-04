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

