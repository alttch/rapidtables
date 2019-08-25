# rapidtables

**rapidtables** is a module for Python 2/3, which does only one thing: converts
lists of dictionaries to pre-formatted tables. And it does the job as fast as
possible.

**rapidtables** is focused on speed and is useful for applications which
dynamically refresh data in console. The module code is heavily optimized, it
uses only tuples inside and on a relatively small tables (<2000 records) it
renders them even faster than Pandas.

And unlike other similar modules, **rapidtables** can output pre-formatted
tuples of strings or even tuples of tuples of strings, which allows you to
colorize every single column.

## Example

```python
from rapidtables import format_table
from termcolor import colored

header, cols = format_table(data, fmt=2) # data is list of dicts
spacer = '  '
print(colored(spacer.join(header), color='blue'))
print(colored('-' * sum([(len(x) + 2) for x in header]), color='grey'))
for c in cols:
    print(colored(c[0], color='white', attrs=['bold']) + spacer, end='')
    print(colored(c[1], color='cyan') + spacer, end='')
    print(colored(c[2], color='yellow'))
```

![colorized table](https://github.com/alttch/rapidtables/blob/master/colored.png?raw=true)

Pretty cool, isn't it? Actually, it was the most complex example, you can
make just

```python
header, rows = format_table(data, fmt=1)
```

and obtain header + table rows already joined. Or you can use *make_table*
function to return the table out-of-the-box (or *print_table* to instantly
print it), and print it in raw:

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

Formats a table. Outputs data in raw, tuple of strings or tuple of tuples of
strings, customize headers, separators etc. *fmt=0* - raw, *1* - tuple of
strings, *2* - tuple of tuples of strings. Read pydoc for more info.

### make_table

Generates a ready to output table. Support basic formats:

```python
table = rapidtables.make_table(table, tablefmt='raw')
```
```
name  salary  job
-----------------------
John    2000  DevOps
Jack    2500  Architect
Ken     1800  Q/A
```

```python
table = rapidtables.make_table(table, tablefmt='simple')
```
```
name  salary  job
----  ------  ---------
John    2000  DevOps
Jack    2500  Architect
Ken     1800  Q/A
``` 

```python
table = rapidtables.make_table(table, tablefmt='md') # Markdown
```
```
| name | salary | job       |
|------|--------|-----------|
| John |   2000 | DevOps    |
| Jack |   2500 | Architect |
| Ken  |   1800 | Q/A       |
```

```python
table = rapidtables.make_table(table, tablefmt='md') # reStructured Text
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

**rapidtables** is written purely in Python, it will loose to Pandas on a large
(3000+ records) tables, but on small it works super fast.

![benchmark](https://github.com/alttch/rapidtables/blob/master/benchmark.png?raw=true)

Enjoy!
