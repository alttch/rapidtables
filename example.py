#!/usr/bin/env python3

data = [{
    'name': 'John',
    'salary': 2000,
    'job': 'DevOps'
}, {
    'name': 'Jack',
    'salary': 2500,
    'job': 'Architect'
}, {
    'name': 'Diana',
    'salary': None,
    'job': 'Student'
}, {
    'name': 'Ken',
    'salary': 1800,
    'job': 'Q/A'
}]

from rapidtables import format_table, print_table
from termcolor import colored

# colorize every single column
header, rows = format_table(data, fmt=2)
spacer = '  '
print(colored(spacer.join(header), color='blue'))
print(colored('-' * sum([(len(x) + 2) for x in header]), color='grey'))
for r in rows:
    print(colored(r[0], color='white', attrs=['bold']) + spacer, end='')
    print(colored(r[1], color='cyan') + spacer, end='')
    print(colored(r[2], color='yellow'))

print()

# colorize only rows, custom header
header, rows = format_table(data,
                            headers=('first name', 'income', 'position'),
                            fmt=1)
print(colored(header, color='blue'))
print(colored('-' * len(header), color='grey'))
for r in rows:
    print(colored(r, color='yellow'))

print()

# print raw
for fmt in ('raw', 'simple', 'md', 'rst'):
    print_table(data, tablefmt=fmt)
    print()
