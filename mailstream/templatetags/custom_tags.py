from django import template
import datetime

register = template.Library()


@register.simple_tag
def mediapath_tag(path):
    if path:
        return f'/media/{path}'
    return '#'


@register.filter(name='mediapath')
def mediapath(path):
    if path:
        return f'/media/{path}'
    return '#'


@register.simple_tag
def this_year(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.filter(name='lookup')
def lookup(my_list, key):
    for item in my_list:
        if str(item[0]) == str(key):
            return item[1]
    return ''


@register.filter(name='is_active')
def is_active(value):
    if value == True:
        return 'Активна'
    return 'Не активна'
