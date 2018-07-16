pylint-django
=============

.. image:: https://travis-ci.org/PyCQA/pylint-django.svg?branch=master
    :target: https://travis-ci.org/PyCQA/pylint-django

.. image:: https://landscape.io/github/landscapeio/pylint-django/master/landscape.png
    :target: https://landscape.io/github/landscapeio/pylint-django

.. image:: https://coveralls.io/repos/PyCQA/pylint-django/badge.svg
    :target: https://coveralls.io/r/PyCQA/pylint-django

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

    pip install pylint-django[with_django]

otherwise sort out your testing environment and please **DO NOT** report issues
about missing Django!


Usage
-----

Ensure ``pylint-django`` is installed and on your path and then execute::

    pylint --load-plugins pylint_django [..other options..] <path_to_your_sources>


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


Additional plugins
------------------

``pylint_django.checkers.db_performance`` looks for migrations which add new
model fields and these fields have a default value. According to
`Django docs <https://docs.djangoproject.com/en/2.0/topics/migrations/#postgresql>`__
this may have performance penalties especially on large tables. The prefered way
is to add a new DB column with ``null=True`` because it will be created instantly
and then possibly populate the table with the desired default values.

Only the last migration from a sub-directory will be examined!

This plugin is disabled by default! To enable it::

    pylint --load-plugins pylint_django --load-plugins pylint_django.checkers.db_performance


Known issues
------------

If you reference foreign-key models by their name (as string) ``pylint-django`` may not be
able to find the model and will report issues because it has no idea what the underlying
type of this field is. If your ``models.py`` itself is not importing the foreign-key class
there's probably some import problem (circular dependencies) preventing referencing the
foreign-key class directly, in which case ``pylint-django`` can't do a huge amount.
If it's just done for convenience that's really up to you the developer to fix.


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

Ideally, add some pylint error suppression messages to the file to prevent
spurious warnings, since these are all tiny little modules not designed to
do anything so there's no need to be perfect.

It is possible to make tests with expected error output, for example, if
adding a new message or simply accepting that pylint is supposed to warn.
A ``test_file_name.txt`` file contains a list of expected error messages in the
format
``error-type:line number:class name or empty:1st line of detailed error text``.


License
-------

``pylint-django`` is available under the GPLv2 license.
