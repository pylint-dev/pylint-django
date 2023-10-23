"""
Setup module for Pylint plugin for Django.
"""
from setuptools import find_packages, setup

with open("README.rst", encoding="utf-8") as readme, open("CHANGELOG.rst", encoding="utf-8") as changelog:
    LONG_DESCRIPTION = readme.read() + "\n" + changelog.read()

TEST_DEPENDENCIES = [
    "pytest>=7.3.1",
    "pytest-cov>=4.0.0",
    "django_tables2>=2.6.0",
    "factory-boy>=3.3.0",
    "django-tastypie>=0.14.6",
    "coverage",
]

DEV_DEPENDENCIES = TEST_DEPENDENCIES + ["twine", "wheel", "tox>=4.5.1"]

setup(
    name="pylint-django",
    url="https://github.com/pylint-dev/pylint-django",
    author="landscape.io",
    author_email="code@landscape.io",
    description="A Pylint plugin to help Pylint understand the Django web framework",
    long_description=LONG_DESCRIPTION,
    version="3.0.0a0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pylint-plugin-utils>=0.8",
        "pylint>=2.13",
    ],
    extras_require={"with_django": ["Django"], "for_tests": TEST_DEPENDENCIES, "for_dev": DEV_DEPENDENCIES},
    license="GPLv2",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
    ],
    keywords=["pylint", "django", "plugin"],
    zip_safe=False,
    project_urls={
        "Repository": "https://github.com/pylint-dev/pylint-django",
        "Changelog": "https://github.com/pylint-dev/pylint-django/blob/master/CHANGELOG.rst",
    },
)
