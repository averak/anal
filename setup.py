from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='anal',
    packages=['anal'],
    install_requires=[],

    version='1.0.0',
    license='MIT',

    author='Tatsuya Abe',
    author_email='abe12@mccc.jp',

    url='https://github.com/averak/anal',

    desription='Utility to standard output based on template and file.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='stdout',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
