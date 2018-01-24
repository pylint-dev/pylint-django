# Changelog

## Version 0.9 (25 Jan 2018)

* Fix [#120](https://github.com/PyCQA/pylint-django/issues/120) -
  TypeError: 'NamesConsumer' object does not support indexing (Simone Basso)
* Fix [#110](https://github.com/PyCQA/pylint-django/issues/120) and
  [#35](https://github.com/PyCQA/pylint-django/issues/120) - resolve
  ForeignKey models specified as strings instead of class names (Mr. Senko)

## Version 0.8.0 (20 Jan 2018)

* This is the last version to support Python 2. Issues a deprecation warning!
* [#109](http://github.com/landscapeio/pylint-django/pull/109),
  adding 'urlpatterns', 'register', 'app_name' to good names. Obsoletes
  [#111](http://github.com/landscapeio/pylint-django/pull/111), fixes
  [#108](http://github.com/landscapeio/pylint-django/issues/108)
  (Vinay Pai)
* Add 'handler500' to good names (Mr. Senko)
* [#103](http://github.com/landscapeio/pylint-django/pull/103):
  Support factory_boy's DjangoModelFactory Meta class (Konstantinos Koukopoulos)
* [#100](https://github.com/landscapeio/pylint-django/pull/100):
  Fix E1101:Instance of '__proxy__' has no 'format' member' when using .format()
  on a ugettext_lazy translation. Fixes
  [#80](https://github.com/landscapeio/pylint-django/issues/80) (canarduck)
* [#99](https://github.com/landscapeio/pylint-django/pull/99):
  Add tests and transforms for DurationField, fixes
  [#95](https://github.com/landscapeio/pylint-django/issues/95) (James M. Allen)
* [#92](https://github.com/landscapeio/pylint-django/pull/92):
  Add json field to WSGIRequest proxy (sjk4sc)
* [#84](https://github.com/landscapeio/pylint-django/pull/84):
  Add support for django.contrib.postgres.fields and UUIDField (Villiers Strauss)
* Stop testing with older Django versions. Currently testing with Django 1.11.x and 2.0
* Stop testing on Python 2, no functional changes in the source code though
* Update tests and require latest version of pylint (>=1.8), fixes
  [#53](https://github.com/landscapeio/pylint-django/issues/53),
  [#97](https://github.com/landscapeio/pylint-django/issues/97)
* [#81](https://github.com/landscapeio/pylint-django/issues/81) Fix 'duplicate-except' false negative
  for except blocks which catch the `DoesNotExist` exception.

## Version 0.7.4
* [#88](https://github.com/landscapeio/pylint-django/pull/88) Fixed builds with Django 1.10 (thanks to [federicobond](https://github.com/federicobond))
* [#91](https://github.com/landscapeio/pylint-django/pull/91) Fixed race condition when running with pylint parallel execution mode (thanks to [jeremycarroll](https://github.com/jeremycarroll))
* [#64](https://github.com/landscapeio/pylint-django/issues/64) "Meta is old style class" now suppressed on BaseSerializer too (thanks to [unklphil](https://github.com/unklphil))
* [#70](https://github.com/landscapeio/pylint-django/pull/70) Updating to handle newer pylint/astroid versions (thanks to [iXce](https://github.com/iXce))

## Version 0.7.2
* [#76](https://github.com/landscapeio/pylint-django/pull/76) Better handling of mongoengine querysetmanager
* [#73](https://github.com/landscapeio/pylint-django/pull/73) (#72)[https://github.com/landscapeio/pylint-django/issues/72] Make package zip safe to help fix some path problems
* [#68](https://github.com/landscapeio/pylint-django/pull/68) Suppressed invalid constant warning for "app_name" in urls.py
* [#67](https://github.com/landscapeio/pylint-django/pull/67) Fix view.args and view.kwargs
* [#66](https://github.com/landscapeio/pylint-django/issues/66) accessing _meta no longer causes a protected-access warning as this is a public API as of Django 1.8
* [#65](https://github.com/landscapeio/pylint-django/pull/65) Add support of mongoengine module.
* [#59](https://github.com/landscapeio/pylint-django/pull/59) Silence old-style-class for widget Meta

## Version 0.7.1
* [#52](https://github.com/landscapeio/pylint-django/issues/52) - Fixed stupid mistake when using versioninfo

## Version 0.7
* [#51](https://github.com/landscapeio/pylint-django/issues/51) - Fixed compatibility with pylint 1.5 / astroid 1.4.1

## Version 0.6.1
* [#43](https://github.com/landscapeio/pylint-django/issues/43) - Foreign key ID access (`somefk_id`) does not raise an 'attribute not found' warning
* [#31](https://github.com/landscapeio/pylint-django/issues/31) - Support for custom model managers (thanks [smirolo](https://github.com/smirolo))
* [#48](https://github.com/landscapeio/pylint-django/pull/48) - Added support for django-restframework (thanks [mbertolacci](https://github.com/mbertolacci))

## Version 0.6
* Pylint 1.4 dropped support for Python 2.6, therefore a constraint is added that pylint-django will only work with Python2.6 if pylint<=1.3 is installed
* [#40](https://github.com/landscapeio/pylint-django/issues/40) - pylint 1.4 warned about View and Model classes not having enough public methods; this is suppressed
* [#37](https://github.com/landscapeio/pylint-django/issues/37) - fixed an infinite loop when using astroid 1.3.3+
* [#36](https://github.com/landscapeio/pylint-django/issues/36) - no longer warning about lack of `__unicode__` method on abstract model classes
* [PR #34](https://github.com/landscapeio/pylint-django/pull/34) - prevent warning about use of `super()` on ModelManager classes

## Version 0.5.5
* [PR #27](https://github.com/landscapeio/pylint-django/pull/27) - better `ForeignKey` transforms, which now work when of the form `othermodule.ModelClass`. This also fixes a problem where an inferred type would be `_Yes` and pylint would fail
* [PR #28](https://github.com/landscapeio/pylint-django/pull/28) - better knowledge of `ManyToManyField` classes

## Version 0.5.4
* Improved resiliance to inference failure when Django types cannot be inferred (which can happen if Django is not on the system path

## Version 0.5.3
* [Issue #25](https://github.com/landscapeio/pylint-django/issues/25) Fixing cases where a module defines `get` as a method

## Version 0.5.2
* Fixed a problem where type inference could get into an infinite loop

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
