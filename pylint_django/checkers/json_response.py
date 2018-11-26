# Copyright (c) 2018 Alexander Todorov <atodorov@MrSenko.com>

# Licensed under the GPL 2.0: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint-django/blob/master/LICENSE
"""
Various suggestions about JSON http responses
"""

import astroid

from pylint import interfaces, checkers
from pylint.checkers import utils
from pylint_django.__pkginfo__ import BASE_ID


class JsonResponseChecker(checkers.BaseChecker):
    """
    Looks for some common patterns when returning http responses containing
    JSON data!
    """

    __implements__ = (interfaces.IAstroidChecker,)

    # configuration section name
    name = 'json-response-checker'
    msgs = {'R%s01' % BASE_ID: ("Instead of HttpResponse(json.dumps(data)) use JsonResponse(data)",
                                'http-response-with-json-dumps',
                                'Used when json.dumps() is used as an argument to HttpResponse().'),
            'R%s02' % BASE_ID: ("Instead of HttpResponse(content_type='application/json') use JsonResponse()",
                                'http-response-with-content-type-json',
                                'Used when HttpResponse() is returning application/json.'),
            'R%s03' % BASE_ID: ("Redundant content_type parameter for JsonResponse()",
                                'redundant-content-type-for-json-response',
                                'Used when JsonResponse() contains content_type parameter. '
                                'This is either redundant or the content_type is not JSON '
                                'which is probably an error.')}

    @utils.check_messages('http-response-with-json-dumps',
                          'http-response-with-content-type-json',
                          'redundant-content-type-for-json-response')
    def visit_call(self, node):
        if (node.func.as_string().endswith('HttpResponse') and node.args
                and isinstance(node.args[0], astroid.Call)
                and node.args[0].func.as_string() == 'json.dumps'):
            self.add_message('http-response-with-json-dumps', node=node)

        if node.func.as_string().endswith('HttpResponse') and node.keywords:
            for keyword in node.keywords:
                if (keyword.arg == 'content_type'
                        and keyword.value.as_string().lower().find('application/json') > -1):
                    self.add_message('http-response-with-content-type-json', node=node)
                    break

        if node.func.as_string().endswith('JsonResponse') and node.keywords:
            for keyword in node.keywords:
                if keyword.arg == 'content_type':
                    self.add_message('redundant-content-type-for-json-response', node=node)
                    break
