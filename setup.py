#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'VERSION'), encoding='utf-8') as f:
    version = f.read()

setup(
    name='python-backlog',
    version=version,
    install_requires=[
        'requests~=2.31.0',
    ],
    description='Backlog API v2 wrapper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='hassaku63',
    author_email='hassaku63@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Natural Language :: Japanese'
    ],
    keywords='nulab backlog',
    url='https://github.com/hassaku63/pbl',
    scripts=[],
    packages=find_packages(exclude=['tests*']),
    python_requires=">=3.8",
    tests_require=[
        "flake8~=6.1.0",
        "tox~=4.11.0",
        "httpretty~=1.1.0",
        "coverage~=7.3.0",
    ],
    project_urls={
        'Source': 'https://github.com/hassaku63/pbl',
    }
)
