import re

with open('example.txt', 'r', encoding='utf-8') as infile:
    for line in infile:
        # Use regex to find all word characters
        words = re.findall(r'\w+', line)
        print(words)
