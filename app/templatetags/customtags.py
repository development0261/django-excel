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


from app.models import permissions
@register.filter
def checkTablePermissioncreate(obj, tableName):
    # print("TEst0")
    # print(tableName.replace(" ","_"))
    # print(permissions.objects.filter(user__in = [obj]).values_list('status',flat=True))
    tableName = tableName.replace(" ","_")
    if permissions.objects.filter(user__in = [obj],status=tableName).exists():
        return permissions.objects.filter(user = obj,status=tableName).first().create
        
        
@register.filter
def checkTablePermissionedit(obj, tableName):
    tableName = tableName.replace(" ","_")
    if permissions.objects.filter(user__in = [obj],status=tableName).exists():
        return permissions.objects.filter(user = obj,status=tableName).first().edit

@register.filter
def checkTablePermissionview(obj, tableName):
    tableName = tableName.replace(" ","_")
    if permissions.objects.filter(user__in = [obj],status=tableName).exists():
        return permissions.objects.filter(user = obj,status=tableName).first().view

@register.filter
def checkTablePermissiondelete(obj, tableName):
    tableName = tableName.replace(" ","_")
    if permissions.objects.filter(user__in = [obj],status=tableName).exists():
        return permissions.objects.filter(user = obj,status=tableName).first().to_delete

@register.filter
def checkTablePermissionmove(obj, tableName):
    tableName = tableName.replace(" ","_")
    if permissions.objects.filter(user__in = [obj],status=tableName).exists():
        return permissions.objects.filter(user = obj,status=tableName).first().move

@register.filter
def checkTablePermissionpublish(obj, tableName):
    tableName = tableName.replace(" ","_")
    if permissions.objects.filter(user__in = [obj],status=tableName).exists():
        return permissions.objects.filter(user = obj,status=tableName).first().publish

