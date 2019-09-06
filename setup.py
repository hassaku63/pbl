#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-backlog',
    version='0.1.1',
    install_requires=[
        'requests>=2.19.1',
        'PyYAML>=3.13'
    ],
    description='Backlog API v2 wrapper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='hassaku63',
    author_email='takuyahashimoto1988@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Natural Language :: Javanese'
    ],
    keywords='nulab backlog',
    url='',
    scripts=[],
    packages=find_packages(exclude=['tests*']),
    tests_require=[
        "httpretty==0.9.5",
        "tox==3.5.2",
        "nose==1.3.7",
        "coverage==4.5.1"
    ]
)
