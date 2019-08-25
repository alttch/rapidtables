#!/usr/bin/env python3

import timeit
import os
from termcolor import colored
from functools import partial

import rapidtables

# install tabulate and pandas modules to do benchmark
import tabulate
import pandas

table = []

pandas.options.display.max_colwidth = 50


def test_rapidtables():
    return rapidtables.make_table(table)


def test_tabulate():
    return tabulate.tabulate(table, headers='keys')


def test_pandas():
    df = pandas.DataFrame(data=table)
    cols = list(df)
    df = df.loc[:, cols]
    idxcol = cols[0]
    df.set_index(idxcol, inplace=True)
    return df.fillna(' ').to_string()


print('Benchmarking')
print()

for rec in (30, 300, 3000, 30000):
    num = 90000 // rec
    print(
        colored(str(rec), color='white',
                attrs=['bold']), 'records table, average render (' +
        colored('milliseconds', color='yellow') + ')\n')
    table.clear()
    for i in range(rec):
        table.append({
            'n': i,
            'txt': 't' * int((i if i < 300 else 300) / 10),
            'zzz': None,
            'numeric': 222,
            'yyy': 'eee {} 333'.format(i)
        })

    result = {}
    outs = '{:.3f}'
    result_rapidtables = timeit.timeit(stmt=test_rapidtables,
                                       number=num) / num * 1000
    result_pandas = timeit.timeit(stmt=test_pandas, number=num) / num * 1000
    result['rapidtables'] = outs.format(result_rapidtables)
    if rec <= 3000:
        result_tabulate = timeit.timeit(stmt=test_tabulate,
                                        number=num) / num * 1000
        result['tabulate'] = outs.format(result_tabulate)
        f1 = '{:.1f}'.format(result_tabulate / result_rapidtables)
    result['pandas'] = outs.format(result_pandas)
    f2 = '{:.1f}'.format(result_pandas / result_rapidtables)
    raw = rapidtables.format_table([result], fmt=1)
    print(colored(raw[0], color='blue'))
    print(colored('-' * len(raw[0]), color='grey'))
    print(colored('\n'.join(raw[1]), color='yellow'))
    print()
    fg = partial(colored, color='green', attrs=['bold'])
    print(colored('rapidtables', color='red', attrs=['bold']) + ': ', end='')
    if rec <= 3000:
        print('{}x faster than tabulate, '.format(fg(f1)), end='')
    print('{}x faster than pandas'.format(fg(f2)))
    print('=' * (os.get_terminal_size(0)[0] - 10))
    print()

print(
    colored('(tables in this test are generated with rapidtables)',
            color='grey',
            attrs=['bold']))
