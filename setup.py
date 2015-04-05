#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup

setup(
    name='h4-scripts',
    version='0.9.0',
    description='Hacking Thursday automation scripts.',
    license='MIT',
    url='https://github.com/hacking-thursday/h4-scripts',
    packages=['h4_scripts'],
    scripts=['bin/h4cli'],
)
