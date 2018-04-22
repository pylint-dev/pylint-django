# Test that using `color_style` or `no_style`
# doesn't raise no-member error
#
# pylint: disable=missing-docstring

from django.core.management.color import color_style, no_style


def function():
    style = color_style()
    print(style.SUCCESS("test"))

    style = no_style()
    print(style.SUCCESS("test"))
