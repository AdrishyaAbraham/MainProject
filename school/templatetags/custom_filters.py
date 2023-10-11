from django import template
import os

register = template.Library()

@register.filter(name='basename')
def basename(value):
    # Check if value is an instance of FieldFile
    if hasattr(value, 'name'):
        return os.path.basename(value.name)
    return os.path.basename(value)
