pylint-django
=============

.. image:: https://github.com/PyCQA/pylint-django/actions/workflows/build.yml/badge.svg
    :target: https://github.com/PyCQA/pylint-django/actions/workflows/build.yml

.. image:: https://coveralls.io/repos/github/PyCQA/pylint-django/badge.svg?branch=master
     :target: https://coveralls.io/github/PyCQA/pylint-django?branch=master

.. image:: https://img.shields.io/pypi/v/pylint-django.svg
    :target: https://pypi.python.org/pypi/pylint-django


About
-----

``pylint-django`` is a `Pylint <http://pylint.org>`__ plugin for improving code
analysis when analysing code using Django. It is also used by the
`Prospector <https://github.com/landscapeio/prospector>`__ tool.


Installation
------------

To install::

    pip install pylint-django


**WARNING:** ``pylint-django`` will not install ``Django`` by default because
this causes more trouble than good,
`see discussion <https://github.com/PyCQA/pylint-django/pull/132>`__. If you wish
to automatically install the latest version of ``Django`` then::

    pip install pylint-django[with-django]

otherwise sort out your testing environment and please **DO NOT** report issues
about missing Django!


Usage
-----


Ensure ``pylint-django`` is installed and on your path. In order to access some
of the internal Django features to improve pylint inspections, you should also
provide a Django settings module appropriate to your project. This can be done
either with an environment variable::

    DJANGO_SETTINGS_MODULE=your.app.settings pylint --load-plugins pylint_django [..other options..] <path_to_your_sources>

Alternatively, this can be passed in as a commandline flag::

    pylint --load-plugins pylint_django --django-settings-module=your.app.settings [..other options..] <path_to_your_sources>

If you do not configure Django, default settings will be used but this will not include, for
example, which applications to include in `INSTALLED_APPS` and so the linting and type inference
will be less accurate. It is recommended to specify a settings module.

Prospector
----------

If you have ``prospector`` installed, then ``pylint-django`` will already be
installed as a dependency, and will be activated automatically if Django is
detected::

    prospector [..other options..]


Features
--------

* Prevents warnings about Django-generated attributes such as
  ``Model.objects`` or ``Views.request``.
* Prevents warnings when using ``ForeignKey`` attributes ("Instance of
  ForeignKey has no <x> member").
* Fixes pylint's knowledge of the types of Model and Form field attributes
* Validates ``Model.__unicode__`` methods.
* ``Meta`` informational classes on forms and models do not generate errors.
* Flags dangerous use of the exclude attribute in ModelForm.Meta.
* Uses Django's internal machinery to try and resolve models referenced as
  strings in ForeignKey fields. That relies on ``django.setup()`` which needs
  the appropriate project settings defined!


Additional plugins
------------------

``pylint_django.checkers.migrations`` looks for migrations which:

- add new model fields and these fields have a default value. According to
  `Django docs <https://docs.djangoproject.com/en/2.0/topics/migrations/#postgresql>`_
  this may have performance penalties especially on large tables. The preferred way
  is to add a new DB column with ``null=True`` because it will be created instantly
  and then possibly populate the table with the desired default values.
  Only the last migration from a sub-directory will be examined;
- are ``migrations.RunPython()`` without a reverse callable - these will result in
  non reversible data migrations;


This plugin is disabled by default! To enable it::

    pylint --load-plugins pylint_django --load-plugins pylint_django.checkers.migrations


Contributing
------------

Please feel free to add your name to the ``CONTRIBUTORS.rst`` file if you want to
be credited when pull requests get merged. You can also add to the
``CHANGELOG.rst`` file if you wish, although we'll also do that when merging.


Tests
-----

The structure of the test package follows that from pylint itself.

It is fairly simple: create a module starting with ``func_`` followed by
a test name, and insert into it some code. The tests will run pylint
against these modules. If the idea is that no messages now occur, then
that is fine, just check to see if it works by running ``scripts/test.sh``.

Any command line argument passed to ``scripts/test.sh`` will be passed to the internal invocation of ``pytest``.
For example if you want to debug the tests you can execute ``scripts/test.sh --capture=no``.
A specific test case can be run by filtering based on the file name of the test case ``./scripts/test.sh -k 'func_noerror_views'``.

Ideally, add some pylint error suppression messages to the file to prevent
spurious warnings, since these are all tiny little modules not designed to
do anything so there's no need to be perfect.

It is possible to make tests with expected error output, for example, if
adding a new message or simply accepting that pylint is supposed to warn.
A ``test_file_name.txt`` file contains a list of expected error messages in the
format
``error-type:line number:class name or empty:1st line of detailed error text:confidence or empty``.


License
-------

``pylint-django`` is available under the GPLv2 license.
