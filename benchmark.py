import timeit
import os
from termcolor import colored
from functools import partial

import rapidtables

# install tabulate and pandas modules to do benchmark
import tabulate
import pandas

num = 100
table = []

pandas.options.display.max_colwidth = 50


def test_rapidtables():
    return rapidtables.format_table(table)


def test_tabulate():
    return tabulate.tabulate(table, headers='keys')


def test_pandas():
    df = pandas.DataFrame(data=table)
    cols = list(df)
    df = df.loc[:, cols]
    idxcol = cols[0]
    df.set_index(idxcol, inplace=True)
    return df.fillna(' ').to_string()


print('Benchmarking, results are in ' + colored('milliseconds', color='yellow'))
print()

for rec in (10, 100, 1000):
    print(colored(str(rec), color='white', attrs=['bold']), 'records table\n')
    table.clear()
    for i in range(rec):
        table.append({
            'n': i,
            'txt': 't' * int(i / 10),
            'zzz': None,
            'numeric': 222,
            'yyy': 'eee {} 333'.format(i)
        })

    result = {}
    outs = '{:.3f}'
    result_rapidtables = timeit.timeit(stmt=test_rapidtables,
                                       number=num) / num * 1000
    result_tabulate = timeit.timeit(stmt=test_tabulate, number=num) / num * 1000
    result_pandas = timeit.timeit(stmt=test_pandas, number=num) / num * 1000
    result['rapidtables'] = outs.format(result_rapidtables)
    result['tabulate'] = outs.format(result_tabulate)
    result['pandas'] = outs.format(result_pandas)
    raw = rapidtables.format_table([result], fmt=1)
    print(colored(raw[0], color='blue'))
    print(colored('-' * len(raw[0]), color='grey'))
    print(colored('\n'.join(raw[1]), color='yellow'))
    print()
    f1 = '{:.1f}'.format(result_tabulate / result_rapidtables)
    f2 = '{:.1f}'.format(result_pandas / result_rapidtables)
    fg = partial(colored, color='green', attrs=['bold'])
    print('{}: x{} faster than tabulate, x{} faster than pandas'.format(
        fg('rapidtables'), fg(f1), fg(f2)))
    print('=' * (os.get_terminal_size(0)[0] - 10))
    print()

print(
    colored('(tables in this test are generated with rapidtables)',
            color='grey',
            attrs=['bold']))
