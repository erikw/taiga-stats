#!/usr/bin/env python3

from setuptools import setup

setup(name='taiga-stats',
    version='0.1',
    description='Generate statistics and charts from Taiga',
    url='TODO',
    author='Erik Westrup',
    author_email='erik.westrup@gmail.com',
    license='BSD',
    install_requires=[
        'python-taiga',
        'numpy',
        'matplotlib',
    ],
)
