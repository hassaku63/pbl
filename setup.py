#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'VERSION'), encoding='utf-8') as f:
    version = f.read().strip()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read().splitlines()

with open(path.join(here, 'requirements-dev.txt'), encoding='utf-8') as f:
    tests_require = f.read().splitlines()

setup(
    name='python-backlog',
    version=version,
    install_requires=install_requires,
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
    tests_require=install_requires + tests_require,
    project_urls={
        'Source': 'https://github.com/hassaku63/pbl',
    }
)
