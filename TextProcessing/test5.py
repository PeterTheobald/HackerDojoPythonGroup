# Copy a file skipping blank lines
input_filename = 'example.txt'
output_filename = 'output.txt'

with open(input_filename, 'r', encoding="latin-1") as infile, open(output_filename, 'w', encoding='utf-8') as outfile:
    for line in infile:
        if line.strip():  # Only write non-blank lines
            outfile.write(line)
