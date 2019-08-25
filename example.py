#!/usr/bin/env python3

# if you need to keep strict column ordering, use OrderedDict for the rows
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
    cols = (
        (colored(r[0], color='white', attrs=['bold'])),
        (colored(r[1], color='cyan')),
        (colored(r[2], color='yellow')))
    print(spacer.join(cols))
print('')

# colorize only rows, custom header. may not work properly, use ordered dicts
# for input data rows
header, rows = format_table(data,
                            headers=('first name', 'income', 'position'),
                            fmt=1)
print(colored(header, color='blue'))
print(colored('-' * len(header), color='grey'))
for r in rows:
    print(colored(r, color='yellow'))

print('')

# print raw, don't align numbers to right for rst
for fmt in ('raw', 'simple', 'md', 'rst'):
    print_table(data, tablefmt=fmt, align=0 if fmt=='rst' else 1)
    print('')
