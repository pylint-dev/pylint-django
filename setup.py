# -*- coding: UTF-8 -*-
"""
Setup module for Pylint plugin for Django.
"""
from setuptools import find_packages, setup

with open("README.rst", encoding="utf-8") as readme, open("CHANGELOG.rst", encoding="utf-8") as changelog:
    LONG_DESCRIPTION = readme.read() + "\n" + changelog.read()

setup(
    name="pylint-django",
    url="https://github.com/PyCQA/pylint-django",
    author="landscape.io",
    author_email="code@landscape.io",
    description="A Pylint plugin to help Pylint understand the Django web framework",
    long_description=LONG_DESCRIPTION,
    version="2.5.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pylint-plugin-utils>=0.7",
        "pylint>=2.0,<3",
    ],
    extras_require={
        "with_django": ["Django"],
        "for_tests": [
            "django_tables2",
            "factory-boy",
            "coverage",
            "pytest",
            "wheel",
            "django-tastypie",
            "pylint>=2.13",
        ],
    },
    license="GPLv2",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
    ],
    keywords=["pylint", "django", "plugin"],
    zip_safe=False,
    project_urls={
        "Changelog": "https://github.com/PyCQA/pylint-django/blob/master/CHANGELOG.rst",
    },
)
