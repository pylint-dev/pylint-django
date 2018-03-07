# -*- coding: UTF-8 -*-
"""
Setup module for Pylint plugin for Django.
"""
import os
from setuptools import setup, find_packages


setup(
    name='pylint-django',
    url='https://github.com/PyCQA/pylint-django',
    author='landscape.io',
    author_email='code@landscape.io',
    description='A Pylint plugin to help Pylint understand the Django web framework',
    version='0.9.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pylint-plugin-utils>=0.2.1',
        'pylint>=1.8.2',
        'Django',
    ],
    license='GPLv2',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['pylint', 'django', 'plugin'],
    zip_safe=False,
)
