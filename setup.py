# -*- coding: UTF-8 -*-
"""
Setup module for Pylint plugin for Django.
"""
from setuptools import setup, find_packages

LONG_DESCRIPTION = open('README.rst').read() + "\n" + open('CHANGELOG.rst').read()

setup(
    name='pylint-django',
    url='https://github.com/PyCQA/pylint-django',
    author='landscape.io',
    author_email='code@landscape.io',
    description='A Pylint plugin to help Pylint understand the Django web framework',
    long_description=LONG_DESCRIPTION,
    version='2.0.10',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pylint-plugin-utils>=0.5',
        'pylint>=2.0',
    ],
    extras_require={
        'with_django': ['Django'],
        'for_tests': ['django_tables2', 'factory-boy', 'coverage', 'pytest'],
    },
    license='GPLv2',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=['pylint', 'django', 'plugin'],
    zip_safe=False,
)
