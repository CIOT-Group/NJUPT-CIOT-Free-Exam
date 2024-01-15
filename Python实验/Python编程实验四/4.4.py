with open('code.txt', 'r') as file:
    lines = file.readlines()

filtered_lines = [line for line in lines if not line.startswith('#')]

with open('new.txt', 'w') as new_file:
    new_file.writelines(filtered_lines)
