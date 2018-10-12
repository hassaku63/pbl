#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='backlog_util',
    version='0.1',
    install_requires=[
        'requests>=2.19.1'
        'PyYAML>=3.13'
    ],
    description='Backlog API v2 wrapper',
    author='hassaku63',
    author_email='takuyahashimoto1988@gmail.com',
    keywords='nulab backlog',
    url='',
    scripts=[],
    packages=find_packages(exclude=['tests*']),
    tests_require=[
        "httpretty<0.9.5",
    ]
)