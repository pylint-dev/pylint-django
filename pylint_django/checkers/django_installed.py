from __future__ import absolute_import
from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages
from pylint_django.__pkginfo__ import BASE_ID


class DjangoInstalledChecker(BaseChecker):
    name = 'django-installed-checker'

    msgs = {
        'F%s01' % BASE_ID: ("Django is not available on the PYTHONPATH",
                            'django-not-available',
                            "Django could not be imported by the pylint-django plugin, so most Django related "
                            "improvements to pylint will fail."),

        'W%s99' % BASE_ID: ('Placeholder message to prevent disabling of checker',
                            'django-not-available-placeholder',
                            'PyLint does not recognise checkers as being enabled unless they have at least'
                            ' one message which is not fatal...')
    }

    @check_messages('django-not-available')
    def close(self):
        try:
            __import__('django')
        except ImportError:
            self.add_message('F%s01' % BASE_ID)
