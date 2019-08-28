#!/usr/bin/env python3

import timeit
import os
from termcolor import colored
from functools import partial
from collections import OrderedDict
from tqdm import tqdm

import sys
from pathlib import Path
sys.path.insert(0, Path().absolute().parent.as_posix())
import rapidtables

table = []
result = []


def test_fixed_align():
    pbar.update(1)
    return rapidtables.make_table(table, align=rapidtables.ALIGN_LEFT)


def test_align_numbers():
    pbar.update(1)
    return rapidtables.make_table(table, align=rapidtables.ALIGN_NUMBERS_RIGHT)


def test_align_numbers_h():
    pbar.update(1)
    return rapidtables.make_table(
        table, align=rapidtables.ALIGN_HOMOGENEOUS_NUMBERS_RIGHT)


def test_align_numbers_h_cols_h():
    pbar.update(1)
    return rapidtables.make_table(
        table,
        align=rapidtables.ALIGN_HOMOGENEOUS_NUMBERS_RIGHT,
        column_width=rapidtables.COLUMN_HOMOGENEOUS_WIDTH_CALC)


def test_all_fixed():
    pbar.update(1)
    return rapidtables.make_table(table,
                                  align=rapidtables.ALIGN_LEFT,
                                  column_width=(20, 20, 20, 20, 20))


def test_align_predefined():
    pbar.update(1)
    return rapidtables.make_table(
        table,
        align=(rapidtables.ALIGN_RIGHT, rapidtables.ALIGN_LEFT,
               rapidtables.ALIGN_LEFT, rapidtables.ALIGN_RIGHT,
               rapidtables.ALIGN_LEFT))


print('Benchmarking\n')

for rec in (30, 300, 3000, 30000):
    num = 9000000 // rec
    for i in range(rec):
        table.append({
            'n': i,
            'txt': 't' * int((i if i < 300 else 300) / 10),
            'zzz': None,
            'numeric': 222,
            'yyy': 'eee {} 333'.format(i)
        })

    with tqdm(total=num * 6, desc=colored(str(rec).rjust(6),
                                          color='white')) as pbar:
        r_fixed = timeit.timeit(stmt=test_fixed_align, number=num) / num * 1000
        r_numbers = timeit.timeit(stmt=test_align_numbers,
                                  number=num) / num * 1000
        r_numbers_h = timeit.timeit(stmt=test_align_numbers_h,
                                    number=num) / num * 1000
        r_predefined = timeit.timeit(stmt=test_align_predefined,
                                     number=num) / num * 1000
        r_numbers_h_col_h = timeit.timeit(stmt=test_align_numbers_h_cols_h,
                                          number=num) / num * 1000
        r_all_fixed = timeit.timeit(stmt=test_all_fixed,
                                    number=num) / num * 1000
    nfmt = '{:.3f}'
    res = OrderedDict()
    res['records'] = rec
    res['align-f'] = nfmt.format(r_fixed)
    res['align-n'] = nfmt.format(r_numbers)
    res['num hom'] = nfmt.format(r_numbers_h)
    res['align-p'] = nfmt.format(r_predefined)
    res['all hom'] = nfmt.format(r_numbers_h_col_h)
    res['all fixed'] = nfmt.format(r_all_fixed)
    result.append(res)

header, rows = rapidtables.format_table(result,
                                        fmt=rapidtables.FORMAT_GENERATOR)
print(colored(header, color='blue'))
print(colored('-' * len(header), color='grey'))
for r in rows:
    print(colored(r, color='yellow'))
