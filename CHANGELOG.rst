Changelog
=========


Version 2.0.10 (07 July 2019), Novi sad etition
-----------------------------------------------

- Suppress ``no-member`` for ``ManyToManyField``. Fix
  `#192 <https://github.com/PyCQA/pylint-django/issues/192>`_ and
  `#237 <https://github.com/PyCQA/pylint-django/issues/237>`_ (Pierre Chiquet)

- Fix ``UnboundLocalError`` with ``ForeignKey(to=)``. Fix
  `#232 <https://github.com/PyCQA/pylint-django/issues/232>`_ (Sardorbek Imomaliev)


Version 2.0.9 (26 April 2019)
-----------------------------

- Fix ``UnboundLocalError: local variable 'key_cls' referenced before assignment``
  for cases when models is a python package, the ``to`` argument is a string
  that is used in this pattern ``app.Model`` and also there is some other
  ``bool`` const like ``null=True`` right after ``to``. (Sardorbek Imomaliev)
- Don't crash if ForeignKey field doesn't have keyword arguments Fix
  `#230 <https://github.com/PyCQA/pylint-django/issues/230>`_


Version 2.0.8 (18 April 2019)
-----------------------------

- Support recursive (self) ForeignKey relations. Fix
  `#208 <https://github.com/PyCQA/pylint-django/issues/208>`_ (Daniil Kharkov)


Version 2.0.7 (16 April 2019)
-----------------------------

- Fixed ``AstroidImportError`` for ``DecimalField``. Fix
  `#221 <https://github.com/PyCQA/pylint-django/issues/221>`_ (Daniil Kharkov)
- Add ``load_configuration()`` in ``pylint_django/__init__.py``. Fix #222
  `#222 <https://github.com/PyCQA/pylint-django/issues/222>`_
- Support ForeignKey relations with ``to`` keyword. Fix
  `#223 <https://github.com/PyCQA/pylint-django/issues/223>`_ (Daniil Kharkov)


Version 2.0.6 (27 Feb 2019)
---------------------------

- Updating dependency version of pylint-plugin-utils as pylint 2.3 release
  was not compatible `#220 <https://github.com/PyCQA/pylint-django/issues/220>`_
- Improvements to tox.ini:
  `#217 <https://github.com/PyCQA/pylint-django/issues/217>`_
  and `#216 <https://github.com/PyCQA/pylint-django/issues/216>`_ (@aerostitch)
- Add support for new load_configuration hook of pylint
  `#214 <https://github.com/PyCQA/pylint-django/issues/214>`_ (@matusvalo)
- 'urlpatterns' no longer reported as an invalid constant name


Version 2.0.5 (17 Dec 2018)
---------------------------

Bumping the version number because there's been a mix-up between
GitHub tags and the versions pushed to PyPI for 2.0.3 and 2.0.4.

Please use 2.0.5 which includes the changes mentioned below!


Version 2.0.4 (do not use)
--------------------------

- Avoid traceback with concurrent execution. Fix
  `#197 <https://github.com/PyCQA/pylint-django/issues/197>`_
- Suppress ``no-member`` errors for ``LazyFunction`` in factories
- Suppress ``no-member`` errors for ``RelatedManager`` fields
- Clean up compatibility code:
  `PR #207 <http://github.com/PyCQA/pylint-django/pull/207>`_


Version 2.0.3 (do not use)
--------------------------

- Fixing compatability between ranges of astroid (2.0.4 -> 2.1) and
  pylint (2.1.1 -> 2.2).
  `#201 <https://github.com/PyCQA/pylint-django/issues/201>`_ and
  `#202 <https://github.com/PyCQA/pylint-django/issues/202>`_

Version 2.0.2 (26 Aug 2018)
---------------------------

- Suppress false-positive no-self-argument in factory.post_generation. Fix
  `#190 <https://github.com/PyCQA/pylint-django/issues/190>`_ (Federico Bond)


Version 2.0.1 (20 Aug 2018)
---------------------------

- Enable testing with Django 2.1
- Add test for Model.objects.get_or_create(). Close
  `#156 <https://github.com/PyCQA/pylint-django/issues/156>`__
- Add test for objects.exclude(). Close
  `#177 <https://github.com/PyCQA/pylint-django/issues/177>`__
- Fix Instance of 'Model' has no 'id' member (no-member),
  fix Class 'UserCreationForm' has no 'declared_fields' member. Close
  `#184 <https://github.com/PyCQA/pylint-django/issues/184>`__
- Fix for Instance of 'ManyToManyField' has no 'add' member. Close
  `#163 <https://github.com/PyCQA/pylint-django/issues/163>`__
- Add test & fix for unused arguments on class based views


Version 2.0 (25 July 2018)
--------------------------

- Requires pylint >= 2.0 which doesn't support Python 2 anymore!
- Add modelform-uses-unicode check to flag dangerous use of the exclude
  attribute in ModelForm.Meta (Federico Bond).


Version 0.11.1 (25 May 2018), the DjangoCon Heidelberg edition
--------------------------------------------------------------

- Enable test case for ``urlpatterns`` variable which was previously disabled
- Disable ``unused-argument`` message for the ``request`` argument passed to
  view functions. Fix
  `#155 <https://github.com/PyCQA/pylint-django/issues/155>`__
- Add transformations for ``model_utils`` managers instead of special-casing them.
  Fix
  `#160 <https://github.com/PyCQA/pylint-django/issues/160>`__


Version 0.11 (18 April 2018), the TestCon Moscow edition
--------------------------------------------------------

- New ``JsonResponseChecker`` that looks for common anti-patterns with
  http responses returning JSON. This includes::

    HttpResponse(json.dumps(data))

    HttpResponse(data, content_type='application/json')

    JsonResponse(data, content_type=...)


Version 0.10.0 (10 April 2018)
------------------------------

- Remove the compatibility layer for older astroid versions
- Make flake8 happy. Fix
  `#102 <https://github.com/PyCQA/pylint-django/issues/102>`__
- Fix: compatibility with Python < 3.6 caused by ``ModuleNotFoundError``
  not available on older versions of Python (Juan Rial)
- Show README and CHANGELOG on PyPI. Fix
  `#122 <https://github.com/PyCQA/pylint-django/issues/122>`__
- Fix explicit unicode check with ``python_2_unicode_compatible`` base models
  (Federico Bond)
- Suppress ``not-an-iterable`` message for 'objects'. Fix
  `#117 <https://github.com/PyCQA/pylint-django/issues/117>`__
- Teach pylint_django that ``objects.all()`` is subscriptable. Fix
  `#144 <https://github.com/PyCQA/pylint-django/issues/144>`__
- Suppress ``invalid-name`` for ``wsgi.application``. Fix
  `#77 <https://github.com/PyCQA/pylint-django/issues/77>`__
- Add test for ``WSGIRequest.context``. Closes
  `#78 <https://github.com/PyCQA/pylint-django/issues/78>`__
- Register transforms for ``FileField``. Fix
  `#60 <https://github.com/PyCQA/pylint-django/issues/60>`__
- New checker ``pylint_django.checkers.db_performance``.
  Enables checking of migrations and reports when there's an
  ``AddField`` operation with a default value which may slow down applying
  migrations on large tables. This may also lead to production tables
  being locked while migrations are being applied. Fix
  `#118 <https://github.com/PyCQA/pylint-django/issues/118>`__
- Suppress ``no-member`` for ``factory.SubFactory`` objects.
  Useful when model factories use ``factory.SubFactory()`` for foreign
  key relations.


Version 0.9.4 (12 March 2018)
-----------------------------

-  Add an optional dependency on Django
-  Fix the ``DjangoInstalledChecker`` so it can actually warn when
   Django isn't available
-  Fix `#136 <https://github.com/PyCQA/pylint-django/issues/136>`__ by
   adding automated build and sanity test scripts

Version 0.9.3 (removed from PyPI)
---------------------------------

-  Fix `#133 <https://github.com/PyCQA/pylint-django/issues/133>`__ and
   `#134 <https://github.com/PyCQA/pylint-django/issues/134>`__ by
   including package data when building wheel and tar.gz packages for
   PyPI (Joseph Herlant)

Version 0.9.2 (broken)
----------------------

-  Fix `#129 <https://github.com/PyCQA/pylint-django/issues/129>`__ -
   Move tests under ``site-packages/pylint_django`` (Mr. Senko)
-  Fix `#96 <https://github.com/PyCQA/pylint-django/issues/96>`__ - List
   Django as a dependency (Mr. Senko)

Version 0.9.1 (26 Feb 2018)
---------------------------

-  Fix `#123 <https://github.com/PyCQA/pylint-django/issues/123>`__ -
   Update links after the move to PyCQA (Mr. Senko)
-  Add test for Meta class from django\_tables2 (Mr. Senko)
-  Fix flake8 complaints (Peter Bittner)
-  Add missing .txt and .rc test files to MANIFEST.in (Joseph Herlant)

Version 0.9 (25 Jan 2018)
-------------------------

-  Fix `#120 <https://github.com/PyCQA/pylint-django/issues/120>`__ -
   TypeError: 'NamesConsumer' object does not support indexing (Simone
   Basso)
-  Fix `#110 <https://github.com/PyCQA/pylint-django/issues/120>`__ and
   `#35 <https://github.com/PyCQA/pylint-django/issues/120>`__ - resolve
   ForeignKey models specified as strings instead of class names (Mr.
   Senko)

Version 0.8.0 (20 Jan 2018)
---------------------------

-  This is the last version to support Python 2. Issues a deprecation
   warning!
-  `#109 <http://github.com/PyCQA/pylint-django/pull/109>`__, adding
   'urlpatterns', 'register', 'app\_name' to good names. Obsoletes
   `#111 <http://github.com/PyCQA/pylint-django/pull/111>`__, fixes
   `#108 <http://github.com/PyCQA/pylint-django/issues/108>`__ (Vinay
   Pai)
-  Add 'handler500' to good names (Mr. Senko)
-  `#103 <http://github.com/PyCQA/pylint-django/pull/103>`__: Support
   factory\_boy's DjangoModelFactory Meta class (Konstantinos
   Koukopoulos)
-  `#100 <https://github.com/PyCQA/pylint-django/pull/100>`__: Fix
   E1101:Instance of '**proxy**\ ' has no 'format' member' when using
   .format() on a ugettext\_lazy translation. Fixes
   `#80 <https://github.com/PyCQA/pylint-django/issues/80>`__
   (canarduck)
-  `#99 <https://github.com/PyCQA/pylint-django/pull/99>`__: Add tests
   and transforms for DurationField, fixes
   `#95 <https://github.com/PyCQA/pylint-django/issues/95>`__ (James M.
   Allen)
-  `#92 <https://github.com/PyCQA/pylint-django/pull/92>`__: Add json
   field to WSGIRequest proxy (sjk4sc)
-  `#84 <https://github.com/PyCQA/pylint-django/pull/84>`__: Add support
   for django.contrib.postgres.fields and UUIDField (Villiers Strauss)
-  Stop testing with older Django versions. Currently testing with
   Django 1.11.x and 2.0
-  Stop testing on Python 2, no functional changes in the source code
   though
-  Update tests and require latest version of pylint (>=1.8), fixes
   `#53 <https://github.com/PyCQA/pylint-django/issues/53>`__,
   `#97 <https://github.com/PyCQA/pylint-django/issues/97>`__
-  `#81 <https://github.com/PyCQA/pylint-django/issues/81>`__ Fix
   'duplicate-except' false negative for except blocks which catch the
   ``DoesNotExist`` exception.

Version 0.7.4
-------------

-  `#88 <https://github.com/PyCQA/pylint-django/pull/88>`__ Fixed builds
   with Django 1.10 (thanks to
   `federicobond <https://github.com/federicobond>`__)
-  `#91 <https://github.com/PyCQA/pylint-django/pull/91>`__ Fixed race
   condition when running with pylint parallel execution mode (thanks to
   `jeremycarroll <https://github.com/jeremycarroll>`__)
-  `#64 <https://github.com/PyCQA/pylint-django/issues/64>`__ "Meta is
   old style class" now suppressed on BaseSerializer too (thanks to
   `unklphil <https://github.com/unklphil>`__)
-  `#70 <https://github.com/PyCQA/pylint-django/pull/70>`__ Updating to
   handle newer pylint/astroid versions (thanks to
   `iXce <https://github.com/iXce>`__)

Version 0.7.2
-------------

-  `#76 <https://github.com/PyCQA/pylint-django/pull/76>`__ Better
   handling of mongoengine querysetmanager
-  `#73 <https://github.com/PyCQA/pylint-django/pull/73>`__
   `#72 <https://github.com/PyCQA/pylint-django/issues/72>`__ Make package
   zip safe to help fix some path problems
-  `#68 <https://github.com/PyCQA/pylint-django/pull/68>`__ Suppressed
   invalid constant warning for "app\_name" in urls.py
-  `#67 <https://github.com/PyCQA/pylint-django/pull/67>`__ Fix
   view.args and view.kwargs
-  `#66 <https://github.com/PyCQA/pylint-django/issues/66>`__ accessing
   \_meta no longer causes a protected-access warning as this is a
   public API as of Django 1.8
-  `#65 <https://github.com/PyCQA/pylint-django/pull/65>`__ Add support
   of mongoengine module.
-  `#59 <https://github.com/PyCQA/pylint-django/pull/59>`__ Silence
   old-style-class for widget Meta

Version 0.7.1
-------------

-  `#52 <https://github.com/PyCQA/pylint-django/issues/52>`__ - Fixed
   stupid mistake when using versioninfo

Version 0.7
-----------

-  `#51 <https://github.com/PyCQA/pylint-django/issues/51>`__ - Fixed
   compatibility with pylint 1.5 / astroid 1.4.1

Version 0.6.1
-------------

-  `#43 <https://github.com/PyCQA/pylint-django/issues/43>`__ - Foreign
   key ID access (``somefk_id``) does not raise an 'attribute not found'
   warning
-  `#31 <https://github.com/PyCQA/pylint-django/issues/31>`__ - Support
   for custom model managers (thanks
   `smirolo <https://github.com/smirolo>`__)
-  `#48 <https://github.com/PyCQA/pylint-django/pull/48>`__ - Added
   support for django-restframework (thanks
   `mbertolacci <https://github.com/mbertolacci>`__)

Version 0.6
-----------

-  Pylint 1.4 dropped support for Python 2.6, therefore a constraint is
   added that pylint-django will only work with Python2.6 if pylint<=1.3
   is installed
-  `#40 <https://github.com/PyCQA/pylint-django/issues/40>`__ - pylint
   1.4 warned about View and Model classes not having enough public
   methods; this is suppressed
-  `#37 <https://github.com/PyCQA/pylint-django/issues/37>`__ - fixed an
   infinite loop when using astroid 1.3.3+
-  `#36 <https://github.com/PyCQA/pylint-django/issues/36>`__ - no
   longer warning about lack of ``__unicode__`` method on abstract model
   classes
-  `PR #34 <https://github.com/PyCQA/pylint-django/pull/34>`__ - prevent
   warning about use of ``super()`` on ModelManager classes

Version 0.5.5
-------------

-  `PR #27 <https://github.com/PyCQA/pylint-django/pull/27>`__ - better
   ``ForeignKey`` transforms, which now work when of the form
   ``othermodule.ModelClass``. This also fixes a problem where an
   inferred type would be ``_Yes`` and pylint would fail
-  `PR #28 <https://github.com/PyCQA/pylint-django/pull/28>`__ - better
   knowledge of ``ManyToManyField`` classes

Version 0.5.4
-------------

-  Improved resiliance to inference failure when Django types cannot be
   inferred (which can happen if Django is not on the system path

Version 0.5.3
-------------

-  `Issue #25 <https://github.com/PyCQA/pylint-django/issues/25>`__
   Fixing cases where a module defines ``get`` as a method

Version 0.5.2
-------------

-  Fixed a problem where type inference could get into an infinite loop

Version 0.5.1
-------------

-  Removed usage of a Django object, as importing it caused Django to
   try to configure itself and thus throw an ImproperlyConfigured
   exception.

Version 0.5
-----------

-  `Issue #7 <https://github.com/PyCQA/pylint-django/issues/7>`__
   Improved handling of Django model fields
-  `Issue #10 <https://github.com/PyCQA/pylint-django/issues/10>`__ No
   warning about missing **unicode** if the Django python3/2
   compatability tools are used
-  `Issue #11 <https://github.com/PyCQA/pylint-django/issues/11>`__
   Improved handling of Django form fields
-  `Issue #12 <https://github.com/PyCQA/pylint-django/issues/12>`__
   Improved handling of Django ImageField and FileField objects
-  `Issue #14 <https://github.com/PyCQA/pylint-django/issues/14>`__
   Models which do not define **unicode** but whose parents do now have
   a new error (W5103) instead of incorrectly warning about no
   **unicode** being present.
-  `Issue #21 <https://github.com/PyCQA/pylint-django/issues/21>`__
   ``ForeignKey`` and ``OneToOneField`` fields on models are replaced
   with instance of the type they refer to in the AST, which allows
   pylint to generate correct warnings about attributes they may or may
   not have.

Version 0.3
-----------

-  Python3 is now supported
-  ``__unicode__`` warning on models does not appear in Python3

Version 0.2
-----------

-  Pylint now recognises ``BaseForm`` as an ancestor of ``Form`` and
   subclasses
-  Improved ``Form`` support
-  `Issue #2 <https://github.com/PyCQA/pylint-django/issues/2>`__ - a
   subclass of a ``Model`` or ``Form`` also has warnings about a
   ``Meta`` class suppressed.
-  `Issue #3 <https://github.com/PyCQA/pylint-django/issues/3>`__ -
   ``Form`` and ``ModelForm`` subclasses no longer warn about ``Meta``
   classes.
