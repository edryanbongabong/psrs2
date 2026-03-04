import os
from django import template

register = template.Library()

@register.filter('has_group')
def has_group(user, group_name):
    group_names = group_name.split(',')
    for group_name in group_names:
        if user.groups.filter(name=group_name.strip()).exists():
            return True
    return False

@register.filter
def get_item(dictionary, key):
    return dictionary[key]