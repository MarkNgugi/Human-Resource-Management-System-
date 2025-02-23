# hrms/templatetags/custom_filters.py
from django import template
from django.forms import BoundField

register = template.Library()

# @register.filter(name='add_class')
# def add_class(value, class_name):
#     """Add a CSS class to a form field."""
#     return value.as_widget(attrs={'class': class_name})




register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    if isinstance(field, BoundField):
        return field.as_widget(attrs={"class": css_class})
    return field