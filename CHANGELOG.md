# Changelog

## Version 0.5.1

* Removed usage of a Django object, as importing it caused Django to try to configure itself and thus throw an ImproperlyConfigured exception.

## Version 0.5

* [Issue #7](https://github.com/landscapeio/pylint-django/issues/7)
Improved handling of Django model fields
* [Issue #10](https://github.com/landscapeio/pylint-django/issues/10)
No warning about missing __unicode__ if the Django python3/2 compatability tools are used
* [Issue #11](https://github.com/landscapeio/pylint-django/issues/11)
Improved handling of Django form fields
* [Issue #12](https://github.com/landscapeio/pylint-django/issues/12)
Improved handling of Django ImageField and FileField objects
* [Issue #14](https://github.com/landscapeio/pylint-django/issues/14)
Models which do not define __unicode__ but whose parents do now have a new error (W5103)
instead of incorrectly warning about no __unicode__ being present.
* [Issue #21](https://github.com/landscapeio/pylint-django/issues/21)
`ForeignKey` and `OneToOneField` fields on models are replaced with instance of the type
they refer to in the AST, which allows pylint to generate correct warnings about attributes
they may or may not have.


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

* [Issue #2](https://github.com/landscapeio/pylint-django/issues/2) - a subclass of a `Model` or `Form` also has
warnings about a `Meta` class suppressed.
* [Issue #3](https://github.com/landscapeio/pylint-django/issues/3) - `Form` and `ModelForm` subclasses no longer
warn about `Meta` classes.
