from django import template

register = template.Library()

@register.filter
def replaceSpacewithUnderScore(value):
    return str(value).replace(" ","_")