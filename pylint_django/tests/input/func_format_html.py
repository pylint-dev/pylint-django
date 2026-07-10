# pylint: disable=missing-docstring, line-too-long, consider-using-f-string, invalid-name

from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

name = "world"
rows = [("a", "b")]


def format_html_with_fstring():
    return format_html(f"<b>{name}</b>")  # [format-html-interpolation]


def format_html_with_str_format():
    return format_html("<b>{}</b>".format(name))  # [format-html-interpolation]


def format_html_with_percent():
    return format_html("<b>%s</b>" % name)  # [format-html-interpolation]


def format_html_with_concat():
    return format_html("<b>" + name + "</b>")  # [format-html-interpolation]


def format_html_join_with_fstring():
    return format_html_join("\n", f"<li>{name}</li>", ((row,) for row in rows))  # [format-html-interpolation]


def mark_safe_with_fstring():
    return mark_safe(f"<b>{name}</b>")  # [mark-safe-interpolation]


# The following are safe and must NOT be flagged.


def format_html_with_arguments():
    return format_html("<b>{}</b>", name)


def format_html_static_literal():
    return format_html("<b>static</b>")


def format_html_static_fstring():
    return format_html(f"static")  # pylint: disable=f-string-without-interpolation


def format_html_join_with_arguments():
    return format_html_join("\n", "<li>{}</li>", ((row,) for row in rows))


def mark_safe_static_literal():
    return mark_safe("<b>static</b>")
