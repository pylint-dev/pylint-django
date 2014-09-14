# Changelog

## Version 0.5

* [Issue #7] Improved handling of Django model fields
* [Issue #11] Improved handling of Django form fields


## Version 0.3

#### New Features

* Python3 is now supported

#### Bugfixes

* `__unicode__` warning on models does not appear in Python3


## Version 0.2

#### New Features

* Pylint now recognises `BaseForm` as an ancestor of `Form` and subclasses
* Improved `Form` support

#### Bugfixes

* [Issue #2](https://github.com/landscapeio/pylint-django/issues/2) - a subclass of a `Model` or `Form` also has warnings about a `Meta` class suppressed.
* [Issue #3](https://github.com/landscapeio/pylint-django/issues/3) - `Form` and `ModelForm` subclasses no longer warn about `Meta` classes.