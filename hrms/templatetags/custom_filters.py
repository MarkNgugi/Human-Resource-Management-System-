# hrms/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, class_name):
    """Add a CSS class to a form field."""
    return value.as_widget(attrs={'class': class_name})
