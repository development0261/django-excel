
from .models import category
from django.contrib import admin
from django.apps import apps
from import_export.admin import ImportExportModelAdmin

from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import *

admin.site.unregister(Group)

# class CustomUserAdmin(UserAdmin):
#     # ...Remove fields by overiding the fieldset value
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
#         (_('Permissions'), {
#         'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#     }),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
# )

# admin.site.register(UserCustom, CustomUserAdmin)

# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
#         (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )

# class CustomGroupAdmin(GroupAdmin):
#     def formfield_for_manytomany(self, db_field, request=None, **kwargs):
#         if db_field.name == 'permissions':
#             qs = kwargs.get('queryset', db_field.remote_field.model.objects)
#             qs = qs.exclude(codename__in=(
#                 'add_permission',
#                 'change_permission',
#                 'delete_permission',

#                 'add_contenttype',
#                 'change_contenttype',
#                 'delete_contenttype',

#                 'add_session',
#                 'delete_session',
#                 'change_session',

#                 'add_logentry',
#                 'change_logentry',
#                 'delete_logentry',
#             ))
#             # Avoid a major performance hit resolving permission names which
#             # triggers a content_type load:
#             kwargs['queryset'] = qs.select_related('content_type')
#         return super(GroupAdmin, self).formfield_for_manytomany(
#             db_field, request=request, **kwargs)


# admin.site.register(User, CustomUserAdmin)
# admin.site.register(Group, CustomGroupAdmin)
# app = apps.get_app_config('app')

# for model_name, model in app.models.items():
#     admin.site.register(model)

@admin.register(content_brief)
class Display(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('topic',)

class customuseradmin(UserAdmin,ImportExportModelAdmin):
     fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Admin User Actions',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (

                    'accessint',

                    
                ),
            },
        ),
    )


# admin.site.register(UserCustom,customuseradmin)

@admin.register(UserCustom)
class UserProfileAdmin(UserAdmin,ImportExportModelAdmin):
    list_display = ['username','email','first_name','last_name','is_staff','is_superuser']
    class Media:
        css = { 'all': ('css/admin.css',) }

    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Admin User Actions',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (

                    'accessint',

                    
                ),
                
            },
        ),
    )
# @admin.register(category)
# class BlogDisplay(admin.ModelAdmin):
#     pass

@admin.register(Ap_Wire)
class BlogDisplay(ImportExportModelAdmin,admin.ModelAdmin):

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px; width:90px;" />'.format(obj.image.url))

    image_tag.short_description = 'image'

    list_display = ["topic", "author","date","status",'image_tag',]
    exclude = ('reverted_count',)

@admin.register(Ap_News)
class BlogDisplay(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("topic", "author","date","status","image")
    exclude = ('reverted_count',)

@admin.register(moreimages_apwire)
class BlogDisplay(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("post",)

@admin.register(moreimages_apnews)
class BlogDisplay(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("post",)

@admin.register(permissions)
class selectiondisplay(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("status",'get_user_permission',"create","edit","view","move","publish","to_delete")

    def get_user_permission(self, obj):
        return " || ".join([p.username for p in obj.user.all()])

    class Media:
       js = (
       'js/admin.js',
       ) 
        


@admin.register(category)
class Display(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("name", )



