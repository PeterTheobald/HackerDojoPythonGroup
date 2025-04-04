import re

# Regex pattern to match phone numbers in common formats (e.g., 123-456-7890, (123) 456-7890)
phone_regex = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')

with open('example.txt', 'r', encoding='utf-8') as infile:
    content = infile.read()
    phone_numbers = re.findall(phone_regex, content)
    for number in phone_numbers:
        print(number)
