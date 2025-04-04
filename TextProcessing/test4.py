with open('illegal.txt', 'r', encoding='utf-8', errors='replace') as file:
    data_replace = file.read()
print("Data read with errors replaced with � symbols:")
print(data_replace)
