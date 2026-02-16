from django import template

register = template.Library()

@register.simple_tag
def index(arr, index):
    return arr[index]