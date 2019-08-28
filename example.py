#!/usr/bin/env python3

# if you need to keep strict column ordering, use OrderedDict for the rows
data = [{
    'name': 'Mike',
    'salary': None,
    'job': 'Student'
}, {
    'name': 'John',
    'salary': 2000,
    'job': 'DevOps'
}, {
    'name': 'Jack',
    'salary': 2500,
    'job': 'Architect'
}, {
    'name': 'Diana',
    'salary': 'N/A',
    'job': 'Student'
}, {
    'name': 'Ken',
    'salary': 1800,
    'job': 'Q/A'
}]

from rapidtables import format_table, print_table
from rapidtables import ALIGN_LEFT, ALIGN_CENTER
from rapidtables import ALIGN_RIGHT, ALIGN_HOMOGENEOUS_RIGHT

from termcolor import colored

# colorize every single column
header, rows = format_table(data, fmt=2, align=ALIGN_HOMOGENEOUS_RIGHT)
spacer = '  '
print(colored(spacer.join(header), color='blue'))
print(colored('-' * sum([(len(x) + 2) for x in header]), color='grey'))
for r in rows:
    cols = ((colored(r[0], color='white', attrs=['bold'])),
            (colored(r[1], color='cyan')), (colored(r[2], color='yellow')))
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

print_table(data, tablefmt='raw', align=(ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT))
print('')
print_table(data, tablefmt='simple', align=ALIGN_LEFT)
print('')
print_table(data, tablefmt='md', align=ALIGN_CENTER)
print('')
print_table(data, tablefmt='rst', align=ALIGN_RIGHT)
print('')
