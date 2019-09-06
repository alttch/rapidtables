#!/usr/bin/env python3

# for testing only, make sure it uses current rapidtables
import sys
from pathlib import Path
sys.path.insert(0, Path().absolute().parent.as_posix())

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
    'name': 'Jack\nDaniels',
    'salary': 2500,
    'job': 'Architect\nCTO\nDevops'
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
from rapidtables import FORMAT_GENERATOR, FORMAT_GENERATOR_COLS
from rapidtables import ALIGN_LEFT, ALIGN_CENTER
from rapidtables import ALIGN_RIGHT, ALIGN_HOMOGENEOUS_NUMBERS_RIGHT
from rapidtables import MULTILINE_ALLOW, MULTILINE_EXTENDED_INFO

from termcolor import colored

# colorize every single column
header, rows = format_table(data,
                            fmt=FORMAT_GENERATOR_COLS,
                            align=ALIGN_HOMOGENEOUS_NUMBERS_RIGHT,
                            multiline=MULTILINE_ALLOW)
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
                            fmt=FORMAT_GENERATOR,
                            multiline=MULTILINE_EXTENDED_INFO)
print(colored(header, color='blue'))
print(colored('-' * len(header), color='grey'))
for r in rows:
    print(colored(r[1], color='white' if r[0] else 'yellow'))

print('')

print_table(data,
            tablefmt='raw',
            align=(ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT),
            allow_multiline=True)
print('')
print_table(data, tablefmt='simple', align=ALIGN_LEFT, allow_multiline=True)
print('')
print_table(data, tablefmt='md', align=ALIGN_CENTER, allow_multiline=True)
print('')
print_table(data, tablefmt='rst', align=ALIGN_RIGHT, allow_multiline=True)
print('')
print_table(data, tablefmt='rstgrid', allow_multiline=True)
print('')
