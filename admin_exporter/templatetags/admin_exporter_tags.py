from django import template
register = template.Library()


@register.simple_tag
def format_name(name):
    return name.replace('_', ' ').capitalize()
