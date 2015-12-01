pylint-django
=============

[![Build Status](https://travis-ci.org/landscapeio/pylint-django.png?branch=master)](https://travis-ci.org/landscapeio/pylint-django) 
[![Code Quality](https://landscape.io/github/landscapeio/pylint-django/master/landscape.png)](https://landscape.io/github/landscapeio/pylint-django)
[![Coverage Status](https://coveralls.io/repos/landscapeio/pylint-django/badge.png)](https://coveralls.io/r/landscapeio/pylint-django)
[![Latest Version](https://img.shields.io/pypi/v/pylint-django.svg)](https://pypi.python.org/pypi/pylint-django)

# About

`pylint-django` is a [Pylint](http://pylint.org) plugin for improving code analysis for when analysing code using Django. It is also used by the [Prospector](https://github.com/landscapeio/prospector) tool.

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

# License

`pylint-django` is available under the GPLv2 license.