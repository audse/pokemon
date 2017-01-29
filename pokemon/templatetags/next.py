from django.template import Library

register = Library()

@register.filter_function
def next(value, arg):
    try:
        return value[int(arg)+1]
    except:
        return None

@register.filter_function
def previous(value, arg):
    try:
        return value[int(arg)-1]
    except:
        return None