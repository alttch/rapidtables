# rapidtables

**rapidtables** is a module for Python 2/3, which does only one thing: converts
lists of dictionaries to pre-formatted tables. And it does the job as fast as
possible.

<img src="https://img.shields.io/pypi/v/rapidtables.svg" /> <img src="https://img.shields.io/badge/license-MIT-green" /> <img src="https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6%20%7C%203.7-blue.svg" />

**rapidtables** is focused on speed and is useful for applications which
dynamically refresh data in console. The module code is heavily optimized, it
uses only tuples inside and on the relatively small tables (<2000 records) it
renders even faster than Pandas.

And unlike other similar modules, **rapidtables** can output pre-formatted
generators of strings or even generators of tuples of strings, which allows you
to colorize every single column.

## Install

```shell
pip install rapidtables
```

## Example

```python
# if you need to keep strict column ordering, use OrderedDict for the rows
data = [
    { 'name': 'John', 'salary': 2000, 'job': 'DevOps' },
    { 'name': 'Jack', 'salary': 2500, 'job': 'Architect' },
    { 'name': 'Diana', 'salary': None, 'job': 'Student' },
    { 'name': 'Ken', 'salary': 1800, 'job': 'Q/A' }
]

from rapidtables import format_table
from termcolor import colored

header, rows = format_table(data, fmt=2)
spacer = '  '
print(colored(spacer.join(header), color='blue'))
print(colored('-' * sum([(len(x) + 2) for x in header]), color='grey'))
for r in rows:
    print(colored(r[0], color='white', attrs=['bold']) + spacer, end='')
    print(colored(r[1], color='cyan') + spacer, end='')
    print(colored(r[2], color='yellow'))
```

![colorized cols](https://github.com/alttch/rapidtables/blob/master/colored.png?raw=true)

Pretty cool, isn't it? Actually, it was the most complex example, you can
work with header + table rows already joined:

```python
header, rows = format_table(data, fmt=1)
print(colored(header, color='blue'))
print(colored('-' * len(header), color='grey'))
for r in rows:
    print(colored(r, color='yellow'))
```

![colorized rows](https://github.com/alttch/rapidtables/blob/master/colored-rows.png?raw=true)

Or you can use *make_table* function to return the table out-of-the-box (or
*print_table* to instantly print it), and print it in raw:

```python
print_table(data)
```

```
name  salary  job
----  ------  ---------
John    2000  DevOps
Jack    2500  Architect
Ken     1800  Q/A
```

## Quick API reference

### format_table

Formats a table. Outputs data in raw, generator of strings (one string per row)
or generator of tuples of strings (one tuple per row, one string per column):

* **fmt=0** raw string
* **fmt=1** generator of strings
* **fmt=2** generator of tuples of strings

You may also customize headers, separators etc. Read pydoc for more
info.

### make_table

Generates a ready to output table. Support basic formats:

```python
table = rapidtables.make_table(data, tablefmt='raw')
```
```
name  salary  job
-----------------------
John    2000  DevOps
Jack    2500  Architect
Ken     1800  Q/A
```

```python
table = rapidtables.make_table(data, tablefmt='simple')
```
```
name  salary  job
----  ------  ---------
John    2000  DevOps
Jack    2500  Architect
Ken     1800  Q/A
``` 

```python
table = rapidtables.make_table(data, tablefmt='md') # Markdown
```
```
| name | salary | job       |
|------|--------|-----------|
| John |   2000 | DevOps    |
| Jack |   2500 | Architect |
| Ken  |   1800 | Q/A       |
```

```python
table = rapidtables.make_table(data, tablefmt='rst') # reStructured Text
```
```
====  ======  =========
name  salary  job
====  ======  =========
John    2000  DevOps
Jack    2500  Architect
Ken     1800  Q/A
====  ======  =========
```

### print_table

The same as *make_table*, but prints table to stdout.

## Benchmarks

**rapidtables** is written purely in Python, it will lose to Pandas on the
large (3000+ records) tables, but on small it works super fast.

![benchmark](https://github.com/alttch/rapidtables/blob/master/benchmark.png?raw=true)

Enjoy!
