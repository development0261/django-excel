from django import template
from pkg_resources import register_finder

register = template.Library()

@register.filter
def replaceSpacewithUnderScore(value):
    return str(value).replace(" ","_")

@register.filter
def validateuser(user,tablename):
    print(user.get_table_role())   
    roles = user.get_table_role()
    tablename=tablename.replace(" ", "_")
    # print(roles[tablename])
    return roles[tablename]

