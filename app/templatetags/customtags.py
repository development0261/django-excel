from django import template
from pkg_resources import register_finder
import re

register = template.Library()

name_dict = {
    "Content Pitching": "Story Pitching",
    "Writing Rewrite": "Writing & Rewriting",
    "Review Draft 1": "First Review",
    "Review Draft 2": "Second Review",
    "FDN Approval 1": "Ready For FDN Approval",
    "Ready For Release": "Ready For Release",
    "App Published": "AP Published"
}

@register.filter
def namereplace(value):
    return name_dict[value]

@register.filter
def desc_count(value):
    desc = value.description
    desc = desc.replace("&nbsp;","")
    desc = desc.replace("&#39;","")
    desc = re.sub('<[^<]*?/?>', '', desc)
    splitdesc = desc.split()
    if not desc:
        return 0
    else:
        return len(splitdesc)


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


@register.filter
def checkDraftStatus(date1,date2):
    from datetime import datetime,timedelta
    print("-------------------------------")
    print(type(date1))
    print(type(date2))
    date2 = datetime.strptime(date2,'%Y-%m-%d')
    delta = date2.date() - date1
    if delta.days > 2:
        return True
    else:
        return False

@register.filter
def imagenameslice(value):
    return value.split("/")[-1]
