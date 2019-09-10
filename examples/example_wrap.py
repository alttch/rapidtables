data = [{
    'rating': 10,
    'job': 'Spiderman'
}, {
    'rating': 9,
    'job': 'Batman'
}, {
    'rating': 8,
    'job': 'Lords of the rings return of the king extended theatrical edition'
}, {
    'rating': 7,
    'job': 'Superman'
}]

from rapidtables import print_table


print_table(data, allow_multiline=True, tablefmt='simple', max_column_width=10, wrap_text=True)
print('')
print_table(data, allow_multiline=True, tablefmt='md', max_column_width=10, wrap_text=True)
print('')
print_table(data, allow_multiline=True, tablefmt='rst', max_column_width=10, wrap_text=True)
print('')
print_table(data, allow_multiline=True, tablefmt='rstgrid', max_column_width=10, wrap_text=True)

