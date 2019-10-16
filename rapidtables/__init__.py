__author__ = "Altertech"
__license__ = "MIT"
__version__ = '0.1.10'

from textwrap import fill
from itertools import chain
from types import GeneratorType

FORMAT_RAW = 0
FORMAT_GENERATOR = 1
FORMAT_GENERATOR_COLS = 2

ALIGN_LEFT = 0
ALIGN_NUMBERS_RIGHT = 1
ALIGN_RIGHT = 2
ALIGN_CENTER = 3
ALIGN_HOMOGENEOUS_NUMBERS_RIGHT = 4

COLUMN_WIDTH_CALC = 0
COLUMN_HOMOGENEOUS_WIDTH_CALC = 1

_TABLEFMT_SIMPLE = 1
_TABLEFMT_MD = 2
_TABLEFMT_RST = 3
_TABLEFMT_RSTGRID = 4

MULTILINE_DENY = 0
MULTILINE_ALLOW = 1
MULTILINE_EXTENDED_INFO = 2


def format_table(table,
                 fmt=FORMAT_RAW,
                 headers=None,
                 separator='  ',
                 align=ALIGN_NUMBERS_RIGHT,
                 column_width=COLUMN_WIDTH_CALC,
                 max_column_width=None,
                 generate_header=True,
                 multiline=MULTILINE_DENY,
                 wrap_text=False,
                 body_sep=None,
                 body_sep_fill='  '):
    '''
    Format list of dicts to table

    If headers are not specified, dict keys MUST be strings

    Args:
        table: list or tuple of dicts
        fmt:
            FORMAT_RAW - raw string (default)
            FORMAT_GENERATOR - generator of strings
            FORMAT_GENERATOR_COLS - generator of tuples of strings
        headers: list or tuple of headers (default: dict keys)
        separator: cell separator (default: "  ")
        align:
            ALIGN_LEFT - align all cols to the left
            ALIGN_NUMBERS_RIGHT (default)_- align numbers to the right
            ALIGN_RIGHT - align all cols to the right
            ALIGN_CENTER - aligh all cols to center
            ALIGN_HOMOGENEOUS_NUMBERS_RIGHT - use first row of data where col
                is not None to determine is col numeric or alpha
            list or tuple of ALIGN_<LEFT|RIGHT|CENTER> - use the specified
                aligns for each column
        column_width:
            COLUMN_WIDTH_CALC (default) - read the entire table to find the
                best width
            COLUMN_HOMOGENEOUS_WIDTH_CALC - use the first row of data where col
                is not None to guess at good column widths
            list or tuple of integers - use the specified widths for each
            column
        max_column_width: maximum column width (default: None - unlimited)
        generate_header: True (default) - create and return header
        multiline:
            MULTILINE_DENY - deny multiline strings (parse as-is)
            MULTILINE_ALLOW - allow multiline strings
            MULTILINE_EXTENDED_INFO - if FORMAT_GENERATOR or
                    FORMAT_GENERATOR_COLS is used, rows are returned in format

                        (bool, row)

                    where bool is True if value is row start and False if it's
                    a helper row with multiline values
        wrap_text: False (default) - Wrap text to multiple lines if its longer
         than max_column_width
        body_sep: char to use as body separator (default: None)
        body_sep_fill: string used to fill body separator to next col

    Returns:
        body if generate_header is False and body_sep is None
        (header, body) if generate_header is True and body_sep is None
        (header, body sep., body) if generate_header is True and body_sep is
                                    not None
        None if table data is empty

        if fmt is set to FORMAT_GENERATOR or FORMAT_GENERATOR_COLS, body is
        returned as generator of strings or generator of tuples
        '''
    if isinstance(table, GeneratorType):
        table = list(table)
    if table:
        if wrap_text:
            if max_column_width is None:
                raise RuntimeError("The 'wrap_text' option require the "
                                   "'max_column_width' to be set as well")
            if multiline == MULTILINE_DENY:
                raise RuntimeError("The 'wrap_text' option require the "
                                   "'multiline' option to be enabled")
        if isinstance(align, int):
            if align == ALIGN_NUMBERS_RIGHT or \
                    align == ALIGN_HOMOGENEOUS_NUMBERS_RIGHT:
                dig_aligns = True
                use_aligns = True
                align_cols = ()
            else:
                dig_aligns = False
                use_aligns = False
        else:
            align_cols = align
            use_aligns = True
            dig_aligns = False
        keys = tuple(table[0])
        len_keysn = len(keys) - 1
        need_body_sep = body_sep is not None
        if fmt == FORMAT_RAW:
            result = ''
        # dig
        if column_width == COLUMN_WIDTH_CALC or \
                column_width == COLUMN_HOMOGENEOUS_WIDTH_CALC:
            key_lengths = ()
            dig_colwidth = True
        else:
            key_lengths = column_width
            dig_colwidth = False
        if dig_aligns or dig_colwidth:
            for ki, k in enumerate(keys):
                if dig_aligns:
                    do_align = None if \
                            align == ALIGN_HOMOGENEOUS_NUMBERS_RIGHT else \
                            ALIGN_RIGHT
                if dig_colwidth:
                    if generate_header:
                        hklen = len(headers[ki]) if headers else len(k)
                    klen = 0
                for r in table:
                    value = r.get(k)
                    if value is not None:
                        if dig_colwidth:
                            if multiline != MULTILINE_DENY and isinstance(
                                    value, str):
                                l = max([
                                    len(z) for z in value.splitlines() or [""]
                                ])
                            else:
                                l = len(str(value))
                            if max_column_width is None:
                                klen = max(klen, l)
                            else:
                                klen = min(max_column_width, max(klen, l))
                        if (align == ALIGN_NUMBERS_RIGHT and
                                do_align == ALIGN_RIGHT) or (
                                    align == ALIGN_HOMOGENEOUS_NUMBERS_RIGHT and
                                    do_align is None):
                            try:
                                float(value)
                                do_align = ALIGN_RIGHT
                            except:
                                do_align = ALIGN_LEFT
                    if (column_width == COLUMN_HOMOGENEOUS_WIDTH_CALC and \
                            klen > 0 and \
                                (not dig_aligns or \
                                (align == ALIGN_HOMOGENEOUS_NUMBERS_RIGHT and \
                                do_align is not None))) or \
                            (align == ALIGN_HOMOGENEOUS_NUMBERS_RIGHT and \
                                do_align is not None and (not dig_colwidth or \
                                (column_width == COLUMN_HOMOGENEOUS_WIDTH_CALC \
                                    and klen > 0))):
                        break
                if dig_colwidth:
                    if generate_header:
                        key_lengths += (max(hklen, klen),)
                    else:
                        key_lengths += (klen,)
                if dig_aligns: align_cols += (do_align,)
        # output
        # add header
        if generate_header:
            if fmt == FORMAT_RAW or fmt == FORMAT_GENERATOR:
                header = ''
                if need_body_sep:
                    bsep = ''
                for i, (ht, key_len) in enumerate(
                        zip(headers if headers else keys, key_lengths)):
                    if need_body_sep:
                        if i < len_keysn:
                            bsep += body_sep * key_len + body_sep_fill
                        else:
                            bsep += body_sep * key_len
                    if (use_aligns and align_cols[i] == ALIGN_RIGHT
                       ) or align == ALIGN_RIGHT:
                        if i < len_keysn:
                            header += ht.rjust(key_len) + separator
                        else:
                            header += ht.rjust(key_len)
                    elif (use_aligns and
                          align_cols[i] == ALIGN_LEFT) or align == ALIGN_LEFT:
                        if i < len_keysn:
                            header += ht.ljust(key_len) + separator
                        else:
                            header += ht.ljust(key_len)
                    else:
                        if i < len_keysn:
                            header += ht.center(key_len) + separator
                        else:
                            header += ht.center(key_len)
            else:
                header = ()
                if need_body_sep:
                    bsep = ()
                for i, (ht, key_len) in enumerate(
                        zip(headers if headers else keys, key_lengths)):
                    if need_body_sep:
                        bsep += ('-' * key_len,)
                    if (use_aligns and align_cols[i] == ALIGN_RIGHT
                       ) or align == ALIGN_RIGHT:
                        header += (ht.rjust(key_len),)
                    elif (use_aligns and
                          align_cols[i] == ALIGN_LEFT) or align == ALIGN_LEFT:
                        header += (ht.ljust(key_len),)
                    else:
                        header += (ht.center(key_len),)

        def body_generator():

            def format_col():
                if col_value is not None:
                    if (use_aligns and align_cols[i] == ALIGN_RIGHT
                       ) or align == ALIGN_RIGHT:
                        return str(col_value)[:max_column_width].rjust(
                            key_lengths[i])
                    elif (use_aligns and
                          align_cols[i] == ALIGN_LEFT) or align == ALIGN_LEFT:
                        return str(col_value)[:max_column_width].ljust(
                            key_lengths[i])
                    else:
                        return str(col_value)[:max_column_width].center(
                            key_lengths[i])
                else:
                    return ' ' * key_lengths[i]

            for v in table:
                if fmt == FORMAT_GENERATOR_COLS:
                    row = ()
                else:
                    row = ''

                if multiline != MULTILINE_DENY: xrow = []
                for i, k in enumerate(keys):
                    col_value = v.get(k)
                    if multiline != MULTILINE_DENY and isinstance(
                            col_value, str):
                        col_vals = col_value.splitlines() or [""]
                        if wrap_text:
                            """
                            Iterate over each line and wrap the text,
                            then combine it all back to a single list.
                            """
                            col_vals = list(
                                chain.from_iterable([
                                    fill(val, max_column_width).splitlines() or
                                    [""] for val in col_vals
                                ]))
                        col_value = col_vals[0]
                        for ci, cv in enumerate(col_vals[1:]):
                            try:
                                xrow[ci][k] = cv
                            except:
                                xrow.append({k: cv})
                    if fmt == FORMAT_GENERATOR_COLS:
                        row += (format_col(),)
                    # FORMAT_GENERATOR
                    elif i < len_keysn:
                        row += format_col() + separator
                    else:
                        row += format_col()
                if multiline == MULTILINE_EXTENDED_INFO:
                    yield True, row
                else:
                    yield row
                if multiline != MULTILINE_DENY and xrow:
                    for x in xrow:
                        if fmt == FORMAT_GENERATOR_COLS:
                            row = ()
                        else:
                            row = ''
                        for i, k in enumerate(keys):
                            col_value = x.get(k)
                            if fmt == FORMAT_GENERATOR_COLS:
                                row += (format_col(),)
                            # FORMAT_GENERATOR
                            elif i < len_keysn:
                                row += format_col() + separator
                            else:
                                row += format_col()
                        if multiline == MULTILINE_EXTENDED_INFO:
                            yield False, row
                        else:
                            yield row

        # add body
        if fmt == FORMAT_RAW:
            result += '\n'.join(body_generator())
        else:
            result = body_generator()
        if generate_header and body_sep:
            return (header, bsep, result)
        elif generate_header:
            return (header, result)
        else:
            return result


def make_table(table,
               tablefmt='simple',
               headers=None,
               align=ALIGN_NUMBERS_RIGHT,
               column_width=COLUMN_WIDTH_CALC,
               max_column_width=None,
               allow_multiline=False,
               wrap_text=False):
    '''
    Generates ready-to-output table

    If headers are not specified, dict keys MUST be strings

    Args:
        table: list or tuple of dicts
        tablefmt: raw, simple (default), md (markdown), rst (reStructuredText)
                  or rstgrid
        headers: list or tuple of headers (default: dict keys)
        align: same as for format_table
        column_width: same as for format_table
        max_column_width: same as for format_table
        allow_multiline: True if multiline strings are allowed
        wrap_text: False (default) - same as format_table
    '''
    if table:
        if tablefmt == 'raw':
            h, t = format_table(table,
                                fmt=FORMAT_RAW,
                                headers=headers,
                                align=align,
                                column_width=column_width,
                                max_column_width=max_column_width,
                                multiline=MULTILINE_ALLOW
                                if allow_multiline else MULTILINE_DENY,
                                wrap_text=wrap_text)
            return h + '\n' + '-' * len(h) + '\n' + t
        else:
            if tablefmt == 'simple':
                body_sep = '-'
                separator = '  '
                body_sep_fill = '  '
                tfmt = _TABLEFMT_SIMPLE
                fmt = FORMAT_GENERATOR
                multiline = MULTILINE_ALLOW if \
                        allow_multiline else MULTILINE_DENY
            elif tablefmt == 'md':
                body_sep = '-'
                separator = ' | '
                body_sep_fill = '-|-'
                tfmt = _TABLEFMT_MD
                fmt = FORMAT_GENERATOR
                multiline = MULTILINE_ALLOW if \
                        allow_multiline else MULTILINE_DENY
            elif tablefmt == 'rst':
                body_sep = '='
                separator = '  '
                body_sep_fill = '  '
                tfmt = _TABLEFMT_RST
                fmt = FORMAT_GENERATOR
                multiline = MULTILINE_ALLOW if \
                        allow_multiline else MULTILINE_DENY
            elif tablefmt == 'rstgrid':
                t = format_table(table,
                                 fmt=FORMAT_GENERATOR_COLS,
                                 headers=headers,
                                 align=align,
                                 column_width=column_width,
                                 max_column_width=max_column_width,
                                 multiline=MULTILINE_EXTENDED_INFO
                                 if allow_multiline else MULTILINE_DENY,
                                 wrap_text=wrap_text)
                if t:
                    r1 = ''
                    r2 = ''
                    h = '| '
                    for x in t[0]:
                        lx = len(x) + 2
                        r1 += '+' + '-' * lx
                        r2 += '+' + '=' * lx
                        h += x + ' | '
                    r1 += '+'
                    r2 += '+'
                    tbody = r2 + '\n'
                    first_row = True
                    for row in t[1]:
                        if allow_multiline:
                            is_first = row[0]
                            row = row[1]
                        if first_row:
                            first_row = False
                        else:
                            tbody += '\n' + (r1 + '\n') if \
                                    not allow_multiline or is_first else '\n'
                        tbody += '| '
                        lr = len(row)
                        for i, col in enumerate(row):
                            tbody += col + ' |'
                            if i < lr:
                                tbody += ' '
                    return r1 + '\n' + h + '\n' + tbody + '\n' + r1
                else:
                    return None
            else:
                raise RuntimeError('table format not supported')
            t = format_table(table,
                             fmt=fmt,
                             headers=headers,
                             align=align,
                             column_width=column_width,
                             max_column_width=max_column_width,
                             multiline=multiline,
                             separator=separator,
                             body_sep_fill=body_sep_fill,
                             body_sep=body_sep,
                             wrap_text=wrap_text)
            if t:
                if tfmt == _TABLEFMT_MD:
                    h = '|-' + t[1] + '-|\n| '
                    return '| ' + t[0] + ' |\n' + h + ' |\n| '.join(t[2]) + ' |'
                elif tfmt == _TABLEFMT_RST:
                    return t[1] + '\n' + t[0] + '\n' + t[1] + '\n' + '\n'.join(
                        t[2]) + '\n' + t[1]
                return t[0] + '\n' + t[1] + '\n' + '\n'.join(t[2])


def print_table(*args, **kwargs):
    '''
    Same as make_table but prints results to stdout
    '''
    t = make_table(*args, **kwargs)
    if t:
        print(t)
