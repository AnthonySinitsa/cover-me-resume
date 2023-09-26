import os
from django import template

register = template.Library()

@register.filter(name='enumerate')
def enumerate_filter(value):
    return enumerate(value)

@register.filter
def filename(value):
    base_name = os.path.splitext(os.path.basename(value))[0]
    # Split the string by underscores and join all parts except the last one.
    return "_".join(base_name.split("_")[:-1])

@register.filter(name='resume_name')
def resume_name(value):
    # Remove the file extension and the directory structure
    return os.path.splitext(value.replace('resumes/', ''))[0]
