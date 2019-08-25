__author__ = "Altertech"
__license__ = "MIT"
__version__ = '0.0.10'

OUT_RAW = 0
OUT_TUPLE = 1
OUT_TT = 2


def format_table(table,
                 fmt=0,
                 headers=None,
                 separator='  ',
                 align=1,
                 generate_header=True,
                 body_sep=None,
                 body_sep_fill='  '):
    '''
    Format list of dicts to table

    If headers are not specified, dict keys MUST be strings

    Args:
        table: list or tuple of dicts
        fmt: 0 - raw (default), 1 - tuple, 2 - tuple of tuples
        headers: list or tuple of headers (default: dict keys)
        separator: cell separator (default: "  ")
        align: 0 - no align, 1 - align decimals to right (default)
        generate_header: True (default) - create and return header
        body_sep: char to use as body separator (default: None)
        body_sep_fill: string used to fill body separator to next col

    Returns:
        result if generate_header is False and body_sep is None
        (header, result) if generate_header is True and body_sep is None
        (header, body sep., result) if generate_header is True and body_sep is
                                    not None
    '''
    calign = align == 0
    if table:
        keys = tuple(table[0])
        len_keys = len(keys)
        lkr = range(len_keys)
        len_keysn = len(keys) - 1
        key_lengths = ()
        if not calign: key_isalpha = ()
        need_body_sep = body_sep is not None
        vals = ()
        if fmt == 0:
            result = ''
        else:
            result = ()
        # dig
        for ki, k in enumerate(keys):
            v = ()
            if generate_header:
                klen = len(headers[ki]) if headers else len(k)
            for ri, r in enumerate(table):
                alpha = False
                value = r.get(k)
                if not alpha:
                    if value is not None:
                        try:
                            float(value)
                        except:
                            alpha = True
                    else:
                        alpha = True
                v += (str(value) if value is not None else '',)
            if generate_header:
                key_lengths += (max(klen, len(max(v, key=len))),)
            else:
                key_lengths += (len(max(v, key=len)),)
            if not calign: key_isalpha += (alpha,)
            vals += (v,)
        # output
        # add header
        if generate_header:
            if fmt == OUT_RAW or fmt == OUT_TUPLE:
                header = ''
                if need_body_sep:
                    bsep = ''
                for i in lkr:
                    if headers:
                        ht = headers[i]
                    else:
                        ht = keys[i]
                    if need_body_sep:
                        if i < len_keysn:
                            bsep += body_sep * key_lengths[i] + body_sep_fill
                        else:
                            bsep += body_sep * key_lengths[i]
                    if calign or key_isalpha[i]:
                        if i < len_keysn:
                            header += ht.ljust(key_lengths[i]) + separator
                        else:
                            header += ht.ljust(key_lengths[i])
                    else:
                        if i < len_keysn:
                            header += ht.rjust(key_lengths[i]) + separator
                        else:
                            header += ht.rjust(key_lengths[i])
            else:
                header = ()
                if need_body_sep:
                    bsep = ()
                for i in lkr:
                    if headers:
                        ht = headers[i]
                    else:
                        ht = keys[i]
                    if need_body_sep:
                        bsep += ('-' * key_lengths[i],)
                    if calign or key_isalpha[i]:
                        header += (ht.ljust(key_lengths[i]),)
                    else:
                        header += (ht.rjust(key_lengths[i]),)
        # add body
        for v in range(len(vals[0])):
            if fmt == OUT_TT:
                row = ()
                ntpl = True
            elif fmt == OUT_TUPLE:
                row = ''
                ntpl = True
            else:
                ntpl = False
            for i in lkr:
                if calign or key_isalpha[i]:
                    r = vals[i][v].ljust(key_lengths[i])
                else:
                    r = vals[i][v].rjust(key_lengths[i])
                if fmt == OUT_TT:
                    row += (r,)
                elif fmt == OUT_TUPLE:
                    if i < len_keysn:
                        row += r + separator
                    else:
                        row += r
                else:
                    result += r + separator
            if ntpl:
                result += (row,)
            else:
                result += '\n'
        if generate_header and body_sep:
            return (header, bsep, result)
        elif generate_header:
            return (header, result)
        else:
            return result


def make_table(table, tablefmt='simple', headers=None, align=1):
    '''
    Generates ready-to-output table

    If headers are not specified, dict keys MUST be strings

    Args:
        table: list or tuple of dicts
        tablefmt: raw, simple (default), md (markdown) or rst (reStructuredText)
        headers: list or tuple of headers (default: dict keys)
        align: 0 - no align, 1 - align decimals to right (default)
    '''
    if tablefmt == 'raw':
        t = format_table(table, fmt=1, headers=headers, align=align)
        return t[0] + '\n' + len(t[0]) * '-' + '\n' + '\n'.join(t[1])
    else:
        if tablefmt == 'simple':
            body_sep = '-'
            separator = '  '
            body_sep_fill = '  '
        elif tablefmt == 'md':
            body_sep = '-'
            separator = ' | '
            body_sep_fill = '-|-'
        elif tablefmt == 'rst':
            body_sep = '='
            separator = '  '
            body_sep_fill = '  '
        else:
            raise RuntimeError('table format not supported')
        t = format_table(table,
                         fmt=1,
                         headers=headers,
                         align=align,
                         separator=separator,
                         body_sep_fill=body_sep_fill,
                         body_sep=body_sep)
        if tablefmt == 'simple':
            return t[0] + '\n' + t[1] + '\n' + '\n'.join(t[2])
        elif tablefmt == 'md':
            h = '|-' + t[1] + '-|\n| '
            return '| ' + t[0] + ' |\n' + h + ' |\n| '.join(t[2]) + ' |'
        if tablefmt == 'rst':
            return t[1] + '\n' + t[0] + '\n' + t[1] + '\n' + '\n'.join(
                t[2]) + '\n' + t[1]


def print_table(table, tablefmt='simple', headers=None, align=1):
    '''
    Same as make_table but prints results to stdout
    '''
    print(make_table(table, tablefmt=tablefmt, headers=headers, align=align))
