__author__ = "Altertech"
__license__ = "MIT"
__version__ = '0.0.24'

OUTPUT_RAW = 0
OUTPUT_GENERATOR = 1
OUTPUT_GENERATOR_TUPLES = 2

_TABLEFMT_SIMPLE = 1
_TABLEFMT_MD = 2
_TABLEFMT_RST = 3


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
        fmt: 0 - raw (default), 1 - generator of strings, 2 - generator of
            tuples
        headers: list or tuple of headers (default: dict keys)
        separator: cell separator (default: "  ")
        align: 0 - no align, 1 - align decimals to right (default)
        generate_header: True (default) - create and return header
        body_sep: char to use as body separator (default: None)
        body_sep_fill: string used to fill body separator to next col

    Returns:
        body if generate_header is False and body_sep is None
        (header, body) if generate_header is True and body_sep is None
        (header, body sep., body) if generate_header is True and body_sep is
                                    not None

        if fmt is set to 1 or 2, body is returned as generator of strings or
        generator of tuples
        '''
    calign = align == 0
    if table:
        keys = tuple(table[0])
        len_keys = len(keys)
        lkr = range(len_keys)
        len_keysn = len_keys - 1
        key_lengths = ()
        if not calign: key_isalpha = ()
        need_body_sep = body_sep is not None
        vals = ()
        if fmt == OUTPUT_RAW:
            result = ''
        # dig
        for ki, k in enumerate(keys):
            v = ()
            alpha = False
            if generate_header:
                klen = len(headers[ki]) if headers else len(k)
            for ri, r in enumerate(table):
                value = r.get(k)
                if not alpha:
                    if value is not None:
                        try:
                            float(value)
                        except:
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
            if fmt == OUTPUT_RAW or fmt == OUTPUT_GENERATOR:
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

        def body_generator():
            for v in range(lv0):
                if fmt == OUTPUT_GENERATOR_TUPLES:
                    row = ()
                else:
                    row = ''
                for i in lkr:
                    if calign or key_isalpha[i]:
                        r = vals[i][v].ljust(key_lengths[i])
                    else:
                        r = vals[i][v].rjust(key_lengths[i])
                    if fmt == OUTPUT_GENERATOR_TUPLES:
                        row += (r,)
                    elif fmt == OUTPUT_GENERATOR:
                        if i < len_keysn:
                            row += r + separator
                        else:
                            row += r
                yield row

        # add body
        lv0 = len(vals[0])
        if fmt == OUTPUT_RAW:
            result += '\n'.join(body_generator(False))
        else:
            result = body_generator()
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
            tfmt = _TABLEFMT_SIMPLE
        elif tablefmt == 'md':
            body_sep = '-'
            separator = ' | '
            body_sep_fill = '-|-'
            tfmt = _TABLEFMT_MD
        elif tablefmt == 'rst':
            body_sep = '='
            separator = '  '
            body_sep_fill = '  '
            tfmt = _TABLEFMT_RST
        else:
            raise RuntimeError('table format not supported')
        t = format_table(table,
                         fmt=1,
                         headers=headers,
                         align=align,
                         separator=separator,
                         body_sep_fill=body_sep_fill,
                         body_sep=body_sep)
        if tfmt == _TABLEFMT_MD:
            h = '|-' + t[1] + '-|\n| '
            return '| ' + t[0] + ' |\n' + h + ' |\n| '.join(t[2]) + ' |'
        elif tfmt == _TABLEFMT_RST:
            return t[1] + '\n' + t[0] + '\n' + t[1] + '\n' + '\n'.join(
                t[2]) + '\n' + t[1]
        if tfmt == _TABLEFMT_SIMPLE:
            return t[0] + '\n' + t[1] + '\n' + '\n'.join(t[2])


def print_table(table, tablefmt='simple', headers=None, align=1):
    '''
    Same as make_table but prints results to stdout
    '''
    print(make_table(table, tablefmt=tablefmt, headers=headers, align=align))
