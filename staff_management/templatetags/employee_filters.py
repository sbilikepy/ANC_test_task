from django import template
from ..models import Employee

register = template.Library()


@register.filter
def get_by_level(employees, level):
    return employees.filter(position__hierarchy_level=level)
