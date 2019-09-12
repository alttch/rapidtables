__version__ = '0.1.6'

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='rapidtables',
    version=__version__,
    author='Altertech',
    author_email='div@altertech.com',
    description=
    'Format/create and print tables from lists of dicts',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alttch/rapidtables',
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=[],
    classifiers=(
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Markup'
    ),
)
