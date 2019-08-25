from rapidtables import format_table, print_table
from termcolor import colored

data = [
    {
        'name': 'John',
        'salary': 2000,
        'job': 'DevOps'
    },
    {
        'name': 'Jack',
        'salary': 2500,
        'job': 'Architect'
    },
    {
        'name': 'Ken',
        'salary': 1800,
        'job': 'Q/A'
    },
]

# colorize every single column
header, cols = format_table(data, fmt=2)
spacer = '  '
print(colored(spacer.join(header), color='blue'))
print(colored('-' * sum([(len(x) + 2) for x in header]), color='grey'))
for c in cols:
    print(colored(c[0], color='white', attrs=['bold']) + spacer, end='')
    print(colored(c[1], color='cyan') + spacer, end='')
    print(colored(c[2], color='yellow'))

print()

# colorize only rows
header, rows = format_table(data, fmt=1)
print(colored(header, color='blue'))
print(colored('-' * len(header), color='grey'))
for r in rows:
    print(colored(r, color='yellow'))

print()

# print raw
print_table(data)
