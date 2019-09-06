#!/usr/bin/env python3

# for testing only, make sure it uses current rapidtables
import sys
# for Python 2 tests - w/o Path
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/..')

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
from rapidtables import FORMAT_GENERATOR, FORMAT_GENERATOR_COLS
from rapidtables import ALIGN_LEFT, ALIGN_CENTER
from rapidtables import ALIGN_RIGHT, ALIGN_HOMOGENEOUS_NUMBERS_RIGHT

from termcolor import colored

# colorize every single column
header, rows = format_table(data,
                            fmt=FORMAT_GENERATOR_COLS,
                            align=ALIGN_HOMOGENEOUS_NUMBERS_RIGHT)
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
                            fmt=FORMAT_GENERATOR)
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
print_table(data, tablefmt='rstgrid')
print('')
