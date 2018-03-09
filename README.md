pylint-django
=============

[![Build Status](https://travis-ci.org/PyCQA/pylint-django.svg?branch=master)](https://travis-ci.org/PyCQA/pylint-django)
[![Code Quality](https://landscape.io/github/landscapeio/pylint-django/master/landscape.png)](https://landscape.io/github/landscapeio/pylint-django)
[![Coverage Status](https://coveralls.io/repos/PyCQA/pylint-django/badge.svg)](https://coveralls.io/r/PyCQA/pylint-django)
[![Latest Version](https://img.shields.io/pypi/v/pylint-django.svg)](https://pypi.python.org/pypi/pylint-django)

# About

`pylint-django` is a [Pylint](http://pylint.org) plugin for improving code analysis for when analysing code using Django. It is also used by the [Prospector](https://github.com/landscapeio/prospector) tool.

# Installation

```
pip install pylint-django
```

**WARNING:** `pylint-django` will not install `Django` by default because this
causes more trouble than good,
[see discussion](https://github.com/PyCQA/pylint-django/pull/132). If you wish
to automatically install the latest version of `Django` then

```
pip install pylint-django[with_django]
```

otherwise sort out your testing environment and please **DO NOT** report issues
about missing Django!

## Usage

#### Pylint

Ensure `pylint-django` is installed and on your path (`pip install pylint-django`), and then run pylint:

```
pylint --load-plugins pylint_django [..other options..]
```

#### Prospector

If you have `prospector` installed, then `pylint-django` will already be installed as a dependency, and will be activated automatically if Django is detected.

```
prospector [..other options..]
```

# Features

* Prevents warnings about Django-generated attributes such as `Model.objects` or `Views.request`.
* Prevents warnings when using `ForeignKey` attributes ("Instance of ForeignKey has no <x> member").
* Fixes pylint's knowledge of the types of Model and Form field attributes
* Validates `Model.__unicode__` methods.
* `Meta` informational classes on forms and models do not generate errors.

# Contributing

Please feel free to add your name to the `CONTRIBUTORS.md` file if you want to be
credited when pull requests get merged. You can also add to the `CHANGELOG.md` file
if you wish, although I'll also do that when merging if not.

## Tests

The structure of the test package follows that from pylint itself.

It is fairly simple: create a module starting with `func_` followed by
a test name, and insert into it some code. The tests will run pylint
 against these modules. If the idea is that no messages now occur, then
 that is fine, just check to see if it works by running `scripts/test.sh`.

Ideally, add some pylint error suppression messages to the file to prevent
spurious warnings, since these are all tiny little modules not designed to
do anything so there's no need to be perfect.

It is possible to make tests with expected error output, for example, if
adding a new message or simply accepting that pylint is supposed to warn.
the `messages` directory contains a list of files which should match the
name of the test and contain error type, line number, class and expected text.
These are useful to quickly add "expected messages".


# License

`pylint-django` is available under the GPLv2 license.