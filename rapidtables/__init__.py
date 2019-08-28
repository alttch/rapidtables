__author__ = "Altertech"
__license__ = "MIT"
__version__ = '0.1.0'

FORMAT_RAW = 0
FORMAT_GENERATOR = 1
FORMAT_GENERATOR_COLS = 2

_TABLEFMT_SIMPLE = 1
_TABLEFMT_MD = 2
_TABLEFMT_RST = 3

ALIGN_LEFT = 0
ALIGN_NUMBERS_RIGHT = 1
ALIGN_RIGHT = 2
ALIGN_CENTER = 3
ALIGN_HOMOGENEOUS_NUMBERS_RIGHT = 4


def format_table(table,
                 fmt=FORMAT_RAW,
                 headers=None,
                 separator='  ',
                 align=ALIGN_NUMBERS_RIGHT,
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
        align: integer or list/tuple
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
    if table:
        if isinstance(align, int):
            if align == ALIGN_NUMBERS_RIGHT or align == ALIGN_HOMOGENEOUS_NUMBERS_RIGHT:
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
        len_keys = len(keys)
        lkr = range(len_keys)
        len_keysn = len_keys - 1
        key_lengths = ()
        need_body_sep = body_sep is not None
        if fmt == FORMAT_RAW:
            result = ''
        # dig
        for ki, k in enumerate(keys):
            if dig_aligns:
                do_align = None if \
                        align == ALIGN_HOMOGENEOUS_NUMBERS_RIGHT else ALIGN_RIGHT
            if generate_header:
                hklen = len(headers[ki]) if headers else len(k)
            klen = 0
            for ri, r in enumerate(table):
                value = r.get(k)
                if value is not None:
                    klen = max(klen, len(str(value)))
                    if (align == ALIGN_NUMBERS_RIGHT and do_align == ALIGN_RIGHT
                       ) or (align == ALIGN_HOMOGENEOUS_NUMBERS_RIGHT and
                             do_align is None):
                        try:
                            float(value)
                            do_align = ALIGN_RIGHT
                        except:
                            do_align = ALIGN_LEFT
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
                    if (use_aligns and align_cols[i] == ALIGN_RIGHT
                       ) or align == ALIGN_RIGHT:
                        if i < len_keysn:
                            header += ht.rjust(key_lengths[i]) + separator
                        else:
                            header += ht.rjust(key_lengths[i])
                    elif (use_aligns and
                          align_cols[i] == ALIGN_LEFT) or align == ALIGN_LEFT:
                        if i < len_keysn:
                            header += ht.ljust(key_lengths[i]) + separator
                        else:
                            header += ht.ljust(key_lengths[i])
                    else:
                        if i < len_keysn:
                            header += ht.center(key_lengths[i]) + separator
                        else:
                            header += ht.center(key_lengths[i])
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
                    if (use_aligns and align_cols[i] == ALIGN_RIGHT
                       ) or align == ALIGN_RIGHT:
                        header += (ht.rjust(key_lengths[i]),)
                    elif (use_aligns and
                          align_cols[i] == ALIGN_LEFT) or align == ALIGN_LEFT:
                        header += (ht.ljust(key_lengths[i]),)
                    else:
                        header += (ht.center(key_lengths[i]),)

        def body_generator():
            for v in table:
                if fmt == FORMAT_GENERATOR_COLS:
                    row = ()
                else:
                    row = ''
                for i, k in enumerate(keys):
                    val = v.get(k)
                    if val is not None:
                        if (use_aligns and align_cols[i] == ALIGN_RIGHT
                           ) or align == ALIGN_RIGHT:
                            r = str(val).rjust(key_lengths[i])
                        elif (use_aligns and align_cols[i] == ALIGN_LEFT
                             ) or align == ALIGN_LEFT:
                            r = str(val).ljust(key_lengths[i])
                        else:
                            r = str(val).center(key_lengths[i])
                    else:
                        r = ' ' * key_lengths[i]
                    if fmt == FORMAT_GENERATOR_COLS:
                        row += (r,)
                    # FORMAT_GENERATOR
                    elif i < len_keysn:
                        row += r + separator
                    else:
                        row += r
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
               align=ALIGN_NUMBERS_RIGHT):
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


def print_table(*args, **kwargs):
    '''
    Same as make_table but prints results to stdout
    '''
    print(make_table(*args, **kwargs))
